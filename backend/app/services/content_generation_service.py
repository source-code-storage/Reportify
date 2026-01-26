"""
Content Generation Service
Uses OpenAI GPT-4 to generate report content based on notes
"""

from typing import List, Dict, Any, Optional
from openai import OpenAI
import tiktoken

from app.core.config import settings
from app.services.embedding_service import get_embedding_service
from app.services.vector_service import get_vector_service


class ContentGenerationService:
    """Service for AI-powered content generation"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.embedding_service = get_embedding_service()
        self.vector_service = get_vector_service()

        # Token counter for cost estimation
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))

    def find_relevant_notes(
        self,
        section_title: str,
        section_description: str,
        report_id: int,
        user_id: int,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find notes relevant to a section using semantic search

        Args:
            section_title: Title of the section
            section_description: Description/context of the section
            report_id: ID of the report
            user_id: ID of the user
            top_k: Number of relevant notes to retrieve

        Returns:
            List of relevant note chunks with scores
        """
        # Create query from section title and description
        query = f"{section_title}. {section_description}"

        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)

        # Search for similar notes
        results = self.vector_service.search_similar(
            query_embedding=query_embedding,
            report_id=report_id,
            user_id=user_id,
            limit=top_k,
        )

        return results

    def build_generation_prompt(
        self,
        section_title: str,
        section_description: str,
        relevant_notes: List[Dict[str, Any]],
        current_content: str = "",
        instruction: str = "generate",
    ) -> str:
        """
        Build the prompt for content generation

        Args:
            section_title: Title of the section
            section_description: Description of the section
            relevant_notes: List of relevant note chunks
            current_content: Existing content (for improve/expand)
            instruction: Type of generation (generate, improve, expand)

        Returns:
            Formatted prompt string
        """
        # Format notes with citations
        notes_text = ""
        for idx, note in enumerate(relevant_notes, 1):
            notes_text += f"\n[Source {idx}: {note['filename']}]\n"
            notes_text += f"{note['chunk_text']}\n"
            notes_text += f"(Relevance: {note['score']:.2f})\n"

        if instruction == "generate":
            prompt = f"""You are an academic writing assistant helping to write a report section.

Section Title: {section_title}
Section Purpose: {section_description}

Research Notes:
{notes_text}

Task: Write a comprehensive, well-structured section based on the research notes above.

Requirements:
- Write in clear, academic style
- Use information from the provided sources
- Include inline citations in the format (Source X)
- Be comprehensive but concise
- Maintain logical flow and structure
- Use appropriate headings if needed

Generate the section content:"""

        elif instruction == "improve":
            prompt = f"""You are an academic writing assistant helping to improve a report section.

Section Title: {section_title}

Current Content:
{current_content}

Research Notes for Reference:
{notes_text}

Task: Improve the content by:
- Enhancing clarity and readability
- Fixing grammar and style issues
- Strengthening arguments
- Ensuring proper citations
- Maintaining the original meaning and structure

Provide the improved version:"""

        elif instruction == "expand":
            prompt = f"""You are an academic writing assistant helping to expand a report section.

Section Title: {section_title}

Current Content:
{current_content}

Additional Research Notes:
{notes_text}

Task: Expand the content by:
- Adding more detail and depth
- Incorporating additional information from the research notes
- Elaborating on key points
- Adding examples or evidence
- Maintaining coherent structure

Provide the expanded version:"""

        else:
            raise ValueError(f"Unknown instruction: {instruction}")

        return prompt

    def generate_content(
        self,
        section_title: str,
        section_description: str = "",
        report_id: int = None,
        user_id: int = None,
        current_content: str = "",
        instruction: str = "generate",
        temperature: float = 0.7,
        max_tokens: int = 1500,
    ) -> Dict[str, Any]:
        """
        Generate content for a section

        Args:
            section_title: Title of the section
            section_description: Description of the section
            report_id: ID of the report
            user_id: ID of the user
            current_content: Existing content (for improve/expand)
            instruction: Type of generation (generate, improve, expand)
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Dict with generated content and metadata
        """
        # Find relevant notes
        relevant_notes = self.find_relevant_notes(
            section_title=section_title,
            section_description=section_description,
            report_id=report_id,
            user_id=user_id,
            top_k=5,
        )

        # Build prompt
        prompt = self.build_generation_prompt(
            section_title=section_title,
            section_description=section_description,
            relevant_notes=relevant_notes,
            current_content=current_content,
            instruction=instruction,
        )

        # Count input tokens
        input_tokens = self.count_tokens(prompt)

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert academic writing assistant. You help students and researchers write high-quality report sections based on their research notes.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Extract generated content
        generated_content = response.choices[0].message.content

        # Count output tokens
        output_tokens = self.count_tokens(generated_content)

        # Calculate cost (approximate, based on GPT-4 pricing)
        # GPT-4: $0.03/1K input tokens, $0.06/1K output tokens
        input_cost = (input_tokens / 1000) * 0.03
        output_cost = (output_tokens / 1000) * 0.06
        total_cost = input_cost + output_cost

        return {
            "content": generated_content,
            "sources": relevant_notes,
            "metadata": {
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "estimated_cost": round(total_cost, 4),
                "instruction": instruction,
            },
        }

    def generate_section_content(
        self, section_title: str, section_description: str, report_id: int, user_id: int
    ) -> Dict[str, Any]:
        """Generate new content for a section"""
        return self.generate_content(
            section_title=section_title,
            section_description=section_description,
            report_id=report_id,
            user_id=user_id,
            instruction="generate",
        )

    def improve_content(
        self, section_title: str, current_content: str, report_id: int, user_id: int
    ) -> Dict[str, Any]:
        """Improve existing content"""
        return self.generate_content(
            section_title=section_title,
            section_description="",
            report_id=report_id,
            user_id=user_id,
            current_content=current_content,
            instruction="improve",
        )

    def expand_content(
        self, section_title: str, current_content: str, report_id: int, user_id: int
    ) -> Dict[str, Any]:
        """Expand existing content with more detail"""
        return self.generate_content(
            section_title=section_title,
            section_description="",
            report_id=report_id,
            user_id=user_id,
            current_content=current_content,
            instruction="expand",
        )


# Global instance
_content_generation_service = None


def get_content_generation_service() -> ContentGenerationService:
    """Get or create the global content generation service instance"""
    global _content_generation_service
    if _content_generation_service is None:
        _content_generation_service = ContentGenerationService()
    return _content_generation_service
