import logging
import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, model_validator
from typing import Literal

from core.alignment import align
from core.scoring import ScoringMatrixFactory
from core.sequence import SequenceTypeFactory, InvalidSequenceEncodingError
from core.sequence_parsing import InputFormatFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

port = int(os.environ.get("PORT", 8000))
origins = os.environ.get(
    "ALLOWED_ORIGINS", f"http://localhost:{port}").split(",")

MAX_SEQUENCE_LENGTH = 50

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


VALID_PRESETS_BY_SEQUENCE_TYPE = {
    "DNA": {"NCBI BLAST (Close)", "NCBI BLAST (Divergent)", "DNAfull"},
    "RNA": {"RIBOSUM"},
    "Protein": set(),
}


class ScoringConfig(BaseModel):
    use_custom: bool
    preset: Literal[
        "default",
        "NCBI BLAST (Close)",
        "NCBI BLAST (Divergent)",
        "DNAfull",
        "RIBOSUM",
    ] = "default"


class AlignRequest(BaseModel):
    mode: Literal["global", "local", "multiple"]
    sequence_type: Literal["DNA", "RNA", "Protein"]
    input_format: Literal["plain", "FASTA"]
    raw_input: str
    scoring: ScoringConfig

    @model_validator(mode="after")
    def validate_raw_input(self):
        if not self.raw_input.strip():
            raise ValueError("raw_input must not be blank")
        return self

    @model_validator(mode="after")
    def validate_scoring_preset(self):
        preset = self.scoring.preset
        if preset == "default":
            return self
        if self.scoring.use_custom:
            raise ValueError(
                "scoring.preset cannot be combined with scoring.use_custom=True")
        if preset not in VALID_PRESETS_BY_SEQUENCE_TYPE.get(self.sequence_type, set()):
            raise ValueError(
                f"{preset!r} is not a valid preset for sequence_type {self.sequence_type!r}")
        return self


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def run_alignment(request: AlignRequest) -> dict[str, str]:

    input_parser = InputFormatFactory.create_input_format(request.input_format)
    raw_sequences = input_parser.clean_sequences(request.raw_input)

    if not raw_sequences:
        raise ValueError("No sequences found in raw_input")

    if any(len(seq) > MAX_SEQUENCE_LENGTH for seq in raw_sequences):
        raise ValueError(
            f"All sequences must have length <= {MAX_SEQUENCE_LENGTH}")

    sequence_type = SequenceTypeFactory.create_sequence_type(
        request.sequence_type)
    validated_sequences = sequence_type.validate_encoding(raw_sequences)

    scoring_matrix = ScoringMatrixFactory.create_scoring_matrix(
        request.scoring.use_custom,
        request.sequence_type,
        None if request.scoring.preset == "default" else request.scoring.preset,
    )

    return align(validated_sequences, scoring_matrix.scoring_matrix, request.mode)


@app.post("/align")
def align_endpoint(request: AlignRequest) -> JSONResponse:

    try:

        trace = run_alignment(request)

    except InvalidSequenceEncodingError as e:
        return JSONResponse(status_code=422, content={
            "error": "invalid_encoding",
            "detail": str(e),
            "offending_index": e.offending_index,
            "offending_char": e.offending_char,
        })

    except ValueError as ve:
        return JSONResponse(status_code=422, content={"error": "invalid_request", "detail": str(ve)})

    except NotImplementedError as nie:
        return JSONResponse(status_code=501, content={"error": "not_implemented", "detail": str(nie)})

    except Exception:
        logger.exception("Unhandled error in align_endpoint")
        return JSONResponse(status_code=500, content={"error": "internal_server_error", "detail": "An unexpected error occurred"})

    return JSONResponse(status_code=200, content=trace)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
