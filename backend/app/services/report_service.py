"""
Report management service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.report import Report, ReportSection
from app.models.user import User
from app.schemas.report import ReportCreate, ReportUpdate


class ReportService:
    """Service for report management operations"""

    @staticmethod
    def create_report(db: Session, user_id: int, report_data: ReportCreate) -> Report:
        """
        Create a new report for a user.

        Args:
            db: Database session
            user_id: ID of the user creating the report
            report_data: Report creation data

        Returns:
            Created report
        """
        report = Report(
            user_id=user_id,
            title=report_data.title,
            description=report_data.description,
            status="draft",
            progress_percentage=0.0,
            total_word_count=0,
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return report

    @staticmethod
    def get_user_reports(
        db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Report]:
        """
        Get all reports for a user.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reports
        """
        return (
            db.query(Report)
            .filter(Report.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_report(db: Session, report_id: int, user_id: int) -> Optional[Report]:
        """
        Get a specific report by ID.

        Args:
            db: Database session
            report_id: Report ID
            user_id: User ID (for authorization)

        Returns:
            Report or None if not found

        Raises:
            HTTPException: If report not found or user not authorized
        """
        report = (
            db.query(Report)
            .filter(Report.id == report_id, Report.user_id == user_id)
            .first()
        )

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
            )

        return report

    @staticmethod
    def update_report(
        db: Session, report_id: int, user_id: int, report_data: ReportUpdate
    ) -> Report:
        """
        Update a report.

        Args:
            db: Database session
            report_id: Report ID
            user_id: User ID (for authorization)
            report_data: Update data

        Returns:
            Updated report

        Raises:
            HTTPException: If report not found or user not authorized
        """
        report = ReportService.get_report(db, report_id, user_id)

        # Update fields
        if report_data.title is not None:
            report.title = report_data.title
        if report_data.description is not None:
            report.description = report_data.description
        if report_data.status is not None:
            report.status = report_data.status

        db.commit()
        db.refresh(report)

        return report

    @staticmethod
    def delete_report(db: Session, report_id: int, user_id: int) -> bool:
        """
        Delete a report.

        Args:
            db: Database session
            report_id: Report ID
            user_id: User ID (for authorization)

        Returns:
            True if deleted

        Raises:
            HTTPException: If report not found or user not authorized
        """
        report = ReportService.get_report(db, report_id, user_id)

        db.delete(report)
        db.commit()

        return True

    @staticmethod
    def calculate_progress(db: Session, report_id: int) -> dict:
        """
        Calculate progress metrics for a report.

        Calculates:
        - Completion percentage based on completed sections
        - Total word count across all sections
        - Number of completed sections
        - Total number of sections

        Args:
            db: Database session
            report_id: Report ID

        Returns:
            Dictionary with progress metrics:
            {
                "progress_percentage": float,
                "total_word_count": int,
                "completed_sections": int,
                "total_sections": int
            }
        """
        sections = (
            db.query(ReportSection).filter(ReportSection.report_id == report_id).all()
        )

        if not sections:
            return {
                "progress_percentage": 0.0,
                "total_word_count": 0,
                "completed_sections": 0,
                "total_sections": 0,
            }

        completed_sections = sum(1 for s in sections if s.is_completed)
        total_sections = len(sections)
        progress_percentage = (completed_sections / total_sections) * 100
        total_word_count = sum(s.word_count for s in sections)

        return {
            "progress_percentage": progress_percentage,
            "total_word_count": total_word_count,
            "completed_sections": completed_sections,
            "total_sections": total_sections,
        }

    @staticmethod
    def update_report_progress(db: Session, report_id: int) -> Report:
        """
        Update report progress based on its sections.

        This method recalculates and updates the progress_percentage
        and total_word_count fields in the report.

        Args:
            db: Database session
            report_id: Report ID

        Returns:
            Updated report
        """
        report = db.query(Report).filter(Report.id == report_id).first()

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
            )

        progress_data = ReportService.calculate_progress(db, report_id)

        report.progress_percentage = progress_data["progress_percentage"]
        report.total_word_count = progress_data["total_word_count"]

        db.commit()
        db.refresh(report)

        return report

    @staticmethod
    def get_report_sections(
        db: Session, report_id: int, user_id: int
    ) -> List[ReportSection]:
        """
        Get all sections for a report.

        Args:
            db: Database session
            report_id: Report ID
            user_id: User ID (for authorization)

        Returns:
            List of report sections ordered by order field

        Raises:
            HTTPException: If report not found or user not authorized
        """
        # Verify report ownership
        ReportService.get_report(db, report_id, user_id)

        sections = (
            db.query(ReportSection)
            .filter(ReportSection.report_id == report_id)
            .order_by(ReportSection.order)
            .all()
        )

        return sections

    @staticmethod
    def create_section(
        db: Session, report_id: int, user_id: int, title: str, order: int
    ) -> ReportSection:
        """
        Create a new section in a report.

        Args:
            db: Database session
            report_id: Report ID
            user_id: User ID (for authorization)
            title: Section title
            order: Section order

        Returns:
            Created section

        Raises:
            HTTPException: If report not found or user not authorized
        """
        # Verify report ownership
        ReportService.get_report(db, report_id, user_id)

        section = ReportSection(
            report_id=report_id,
            title=title,
            content="",
            order=order,
            word_count=0,
            is_completed=False,
        )

        db.add(section)
        db.commit()
        db.refresh(section)

        # Update report progress
        ReportService.update_report_progress(db, report_id)

        return section

    @staticmethod
    def update_section(
        db: Session,
        report_id: int,
        section_id: int,
        user_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        order: Optional[int] = None,
        is_completed: Optional[bool] = None,
    ) -> ReportSection:
        """
        Update a report section.

        Args:
            db: Database session
            report_id: Report ID
            section_id: Section ID
            user_id: User ID (for authorization)
            title: New title (optional)
            content: New content (optional)
            order: New order (optional)
            is_completed: New completion status (optional)

        Returns:
            Updated section

        Raises:
            HTTPException: If report or section not found, or user not authorized
        """
        # Verify report ownership
        ReportService.get_report(db, report_id, user_id)

        # Get section
        section = (
            db.query(ReportSection)
            .filter(
                ReportSection.id == section_id, ReportSection.report_id == report_id
            )
            .first()
        )

        if not section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Section not found"
            )

        # Update fields
        if title is not None:
            section.title = title
        if content is not None:
            section.content = content
            # Update word count
            section.word_count = len(content.split())
        if order is not None:
            section.order = order
        if is_completed is not None:
            section.is_completed = is_completed

        db.commit()
        db.refresh(section)

        # Update report progress
        ReportService.update_report_progress(db, report_id)

        return section
