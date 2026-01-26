"""
Content generation service using LLM (OpenAI/Anthropic)
"""

from typing import List, Dict, Optional, Tuple
import json

from app.core.config import settings


class ContentService:
    """Service for AI-powered content generation"""

    def __init__(self):
        """Initialize content service"""
        self._client = None
        self._model = settings.OPENAI_MODEL or "gpt-4"

    @property
    def client(self):
        """Lazy load OpenAI client"""
        if self._client is None:
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except ImportError:
                raise ImportError(
                    "openai is required. Install with: pip install openai"
                )
        return self._client

    def generate_section_content(
        self,
        section_title: str,
        section_description: str = "",
        relevant_notes: List[Dict] = None,
        template_context: str = "",
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> Tuple[str, List[Dict]]:
        """
        Generate content for a report section.

        Args:
            section_title: Title of the section
            section_description: Description or requirements for the section
            relevant_notes: List of relevant notes with content
            template_context: Context from the template
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0-1)

        Returns:
            Tuple of (generated_content, citations)
        """
        # Build context from notes
        notes_context = ""
        citations = []

        if relevant_notes:
            notes_context = "\n\nRelevant source materials:\n"
            for i, note in enumerate(relevant_notes, 1):
                note_content = note.get("content", "")[:1000]  # Limit each note
                notes_context += f"\n[Source {i}] ({note.get('filename', 'Unknown')}):\n{note_content}\n"
                citations.append(
                    {
                        "index": i,
                        "filename": note.get("filename", "Unknown"),
                        "note_id": note.get("id"),
                        "excerpt": (
                            note_content[:200] + "..."
                            if len(note_content) > 200
                            else note_content
                        ),
                    }
                )

        # Build prompt
        prompt = f"""You are a professional report writer. Generate content for the following section of a report.

Section Title: {section_title}
{f'Section Description: {section_description}' if section_description else ''}
{f'Template Context: {template_context}' if template_context else ''}
{notes_context}

Instructions:
1. Write professional, well-structured content for this section
2. Use the source materials provided to support your writing
3. Include inline citations like [Source 1], [Source 2] when referencing materials
4. Maintain a formal, academic tone
5. Be concise but comprehensive
6. Do not make up facts - only use information from the provided sources

Generate the content for the "{section_title}" section:"""

        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional report writer who creates well-structured, citation-backed content.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )

            generated_content = response.choices[0].message.content
            return generated_content, citations

        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")

    def improve_content(
        self, content: str, improvement_type: str = "general", instructions: str = ""
    ) -> str:
        """
        Improve existing content.

        Args:
            content: Content to improve
            improvement_type: Type of improvement (general, clarity, conciseness, formal, expand)
            instructions: Additional instructions

        Returns:
            Improved content
        """
        improvement_prompts = {
            "general": "Improve the overall quality, clarity, and flow of this text.",
            "clarity": "Make this text clearer and easier to understand.",
            "conciseness": "Make this text more concise while keeping the key information.",
            "formal": "Make this text more formal and professional.",
            "expand": "Expand this text with more details and examples.",
        }

        base_instruction = improvement_prompts.get(
            improvement_type, improvement_prompts["general"]
        )

        prompt = f"""{base_instruction}
{f'Additional instructions: {instructions}' if instructions else ''}

Original text:
{content}

Improved text:"""

        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional editor who improves text quality.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=len(content) + 500,
                temperature=0.5,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Failed to improve content: {str(e)}")

    def regenerate_content(
        self,
        section_title: str,
        current_content: str,
        feedback: str = "",
        relevant_notes: List[Dict] = None,
    ) -> Tuple[str, List[Dict]]:
        """
        Regenerate content with feedback.

        Args:
            section_title: Title of the section
            current_content: Current content to regenerate
            feedback: User feedback for regeneration
            relevant_notes: List of relevant notes

        Returns:
            Tuple of (regenerated_content, citations)
        """
        notes_context = ""
        citations = []

        if relevant_notes:
            notes_context = "\n\nSource materials:\n"
            for i, note in enumerate(relevant_notes, 1):
                note_content = note.get("content", "")[:1000]
                notes_context += f"\n[Source {i}] ({note.get('filename', 'Unknown')}):\n{note_content}\n"
                citations.append(
                    {
                        "index": i,
                        "filename": note.get("filename", "Unknown"),
                        "note_id": note.get("id"),
                        "excerpt": (
                            note_content[:200] + "..."
                            if len(note_content) > 200
                            else note_content
                        ),
                    }
                )

        prompt = f"""Regenerate the content for this report section based on the feedback provided.

Section Title: {section_title}

Current Content:
{current_content}

User Feedback: {feedback if feedback else 'Please regenerate with a different approach.'}
{notes_context}

Instructions:
1. Address the user's feedback
2. Maintain professional quality
3. Use source materials and include citations [Source N]
4. Keep the same general structure unless feedback suggests otherwise

Regenerated content:"""

        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional report writer who regenerates content based on feedback.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            return response.choices[0].message.content, citations

        except Exception as e:
            raise Exception(f"Failed to regenerate content: {str(e)}")

    def expand_content(
        self, content: str, target_length: str = "double", focus_areas: List[str] = None
    ) -> str:
        """
        Expand content with more details.

        Args:
            content: Content to expand
            target_length: Target length (double, triple, or specific word count)
            focus_areas: Areas to focus expansion on

        Returns:
            Expanded content
        """
        focus_instruction = ""
        if focus_areas:
            focus_instruction = (
                f"\nFocus on expanding these areas: {', '.join(focus_areas)}"
            )

        prompt = f"""Expand the following text to approximately {target_length} its current length.
{focus_instruction}

Add more:
- Details and examples
- Supporting arguments
- Transitions between ideas
- Context and background

Original text:
{content}

Expanded text:"""

        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional writer who expands text with relevant details.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=len(content) * 3,
                temperature=0.6,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Failed to expand content: {str(e)}")

    def summarize_notes(self, notes: List[Dict], max_length: int = 500) -> str:
        """
        Summarize multiple notes into a concise overview.

        Args:
            notes: List of notes to summarize
            max_length: Maximum length of summary

        Returns:
            Summary text
        """
        if not notes:
            return "No notes available to summarize."

        notes_text = "\n\n".join(
            [
                f"Note from {note.get('filename', 'Unknown')}:\n{note.get('content', '')[:1000]}"
                for note in notes
            ]
        )

        prompt = f"""Summarize the following notes into a concise overview (max {max_length} words):

{notes_text}

Summary:"""

        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional summarizer who creates concise, accurate summaries.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_length * 2,
                temperature=0.3,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Failed to summarize notes: {str(e)}")


# Singleton instance
content_service = ContentService()
