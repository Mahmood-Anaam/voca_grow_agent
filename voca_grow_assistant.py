import asyncio
import logging
from typing import Optional

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    llm,
    multimodal,
)
from livekit.plugins import google, noise_cancellation
from prompts import _SYSTEM_EN_PROMPT, _SYSTEM_AR_PROMPT


logger = logging.getLogger("voca-grow-assistant")
# Define the speaking frame rate for different states
SPEAKING_FRAME_RATE = 1.0
NOT_SPEAKING_FRAME_RATE = 0.5
# Define the character voice mapping
CHARACTER_VOICE_MAP = {
    "WOODY": "Puck",
    "SPIDERMAN": "Fenrir",
    "SNOW": "Aoede",
    "ELSA": "Kore",
}

class VocaGrowAssistant:
    def __init__(self):
        self.agent: Optional[multimodal.MultimodalAgent] = None
        self.model: Optional[google.beta.realtime.RealtimeModel] = None
        self._is_user_speaking: bool = False

    async def start(self, ctx: JobContext):
        """Initialize and start the VocaGrow assistant."""
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        participant = await ctx.wait_for_participant()

        # Wait for initial attributes (lang, character, activitie)
        settings = await self._wait_for_initial_settings(ctx, participant)
        lang=settings.get("lang", "ar")
        character=settings.get("character", "Spiderman")
        activitie=settings.get("activitie", "Shapes")

        # Generate system prompt based on received settings
        system_prompt = _SYSTEM_AR_PROMPT if lang == "ar" else _SYSTEM_EN_PROMPT
        system_prompt = system_prompt.format(character=character, activitie=activitie).strip()
 
        # Initialize the chat model
        chat_ctx = llm.ChatContext()
        self.model = google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",
            voice=CHARACTER_VOICE_MAP.get(character.upper(), "Puck"),
            temperature=0.8,
            instructions=system_prompt,
        )

        # Start the multimodal agent
        self.agent = multimodal.MultimodalAgent(
            model=self.model,
            chat_ctx=chat_ctx,
            noise_cancellation=noise_cancellation.BVC(),
        )
        self.agent.start(ctx.room, participant)

        # Register event handlers
        self.agent.on("user_started_speaking", self._on_user_started_speaking)
        self.agent.on("user_stopped_speaking", self._on_user_stopped_speaking)

    async def _wait_for_initial_settings(self, ctx: JobContext, participant):
        """Wait for participant attributes to be populated."""
        settings = {}

        # If attributes already exist, use them
        if participant.attributes:
            settings = participant.attributes
            return settings

        # Define listener for attribute changes
        event = asyncio.Event()

        def on_participant_attributes_changed(changed_attrs: dict[str, str], p):
            nonlocal settings
            if p.identity == participant.identity:
                logger.info(f"Received updated attributes: {p.attributes}")
                settings = p.attributes
                event.set()

        ctx.room.on("participant_attributes_changed", on_participant_attributes_changed)

        try:
            logger.info("Waiting for participant attributes...")
            await asyncio.wait_for(event.wait(), timeout=30.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for participant attributes.")
        finally:
            ctx.room.off("participant_attributes_changed",on_participant_attributes_changed)

        return settings

    def _get_frame_interval(self) -> float:
        """Get the interval between video frames based on speaking state."""
        return 1.0 / (SPEAKING_FRAME_RATE if self._is_user_speaking else NOT_SPEAKING_FRAME_RATE)

    def _on_user_started_speaking(self):
        """Handler when the user starts speaking."""
        self._is_user_speaking = True
        logger.debug("User started speaking")

    def _on_user_stopped_speaking(self):
        """Handler when the user stops speaking."""
        self._is_user_speaking = False
        logger.debug("User stopped speaking")
