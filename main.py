# python main.py dev
import logging

from dotenv import load_dotenv
from livekit.agents import (
    JobContext,
    WorkerOptions,
    cli,
)

from voca_grow_assistant import VocaGrowAssistant

load_dotenv(".env")

logger = logging.getLogger("voca-grow-assistant")
logger.setLevel(logging.INFO)


async def entrypoint(ctx: JobContext):
    assistant = VocaGrowAssistant()
    await assistant.start(ctx)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
