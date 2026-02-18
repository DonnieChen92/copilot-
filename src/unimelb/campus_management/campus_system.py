"""
Campus Management System
=========================
Unified campus operations for UniMelb AI Platform.

Integrates academic timetabling, room booking, facility management,
student services, and staff administration under one system,
connected to Microsoft Teams and the property management module.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class CampusLocation(Enum):
    """UniMelb campus locations."""

    PARKVILLE = "parkville"
    SOUTHBANK = "southbank"
    BURNLEY = "burnley"
    CRESWICK = "creswick"
    DOOKIE = "dookie"
    WERRIBEE = "werribee"
    SHEPPARTON = "shepparton"


class FacilityType(Enum):
    """Types of campus facilities."""

    LECTURE_THEATRE = "lecture_theatre"
    TUTORIAL_ROOM = "tutorial_room"
    LABORATORY = "laboratory"
    LIBRARY = "library"
    STUDY_SPACE = "study_space"
    OFFICE = "office"
    MEETING_ROOM = "meeting_room"
    COMMON_AREA = "common_area"
    SPORTS_FACILITY = "sports_facility"
    DINING = "dining"
    RETAIL = "retail"


class BookingStatus(Enum):
    """Room/facility booking status."""

    AVAILABLE = "available"
    BOOKED = "booked"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    BLOCKED = "blocked"


@dataclass
class Facility:
    """A campus facility (room, lab, theatre, etc.)."""

    facility_id: str
    name: str
    facility_type: FacilityType
    campus: CampusLocation
    building: str
    level: str
    capacity: int = 0
    equipment: list[str] = field(default_factory=list)
    accessibility: bool = True
    teams_room_id: str = ""  # Microsoft Teams Room resource
    booking_status: BookingStatus = BookingStatus.AVAILABLE
    managed_by: str = ""  # agent: Lendlease, JLL, or internal


@dataclass
class StaffMember:
    """A university staff member (academic or professional)."""

    staff_id: str
    name: str
    email: str
    role_type: str  # "academic" | "professional"
    faculty: str
    department: str
    title: str = ""
    office_location: str = ""
    entra_id: str = ""
    teams_id: str = ""
    phone: str = ""
    research_areas: list[str] = field(default_factory=list)


@dataclass
class ServiceRequest:
    """A campus service request from staff or students."""

    request_id: str
    requester_id: str
    requester_type: str  # "student" | "academic_staff" | "professional_staff"
    service_type: str  # "it_support" | "facility" | "hr" | "finance" | "general"
    subject: str
    description: str
    campus: CampusLocation = CampusLocation.PARKVILLE
    status: str = "open"  # open | assigned | in_progress | resolved | closed
    priority: str = "medium"
    assigned_to: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: datetime | None = None
    ai_suggested_resolution: str = ""


class CampusManagementSystem:
    """
    Campus management system for UniMelb AI Platform.

    Provides:
    - Facility and room management
    - Staff directory and administration
    - Service request handling (AI-assisted)
    - Integration with MS Teams (room resources, calendars)
    - Integration with property management (Lendlease/JLL/MICM)
    """

    def __init__(self) -> None:
        self._facilities: dict[str, Facility] = {}
        self._staff: dict[str, StaffMember] = {}
        self._service_requests: list[ServiceRequest] = {}
        self._request_counter = 0

    # ── Facility Management ──────────────────────────────────────────

    def register_facility(self, facility: Facility) -> Facility:
        """Register a campus facility."""
        self._facilities[facility.facility_id] = facility
        return facility

    def find_facilities(
        self,
        campus: CampusLocation | None = None,
        facility_type: FacilityType | None = None,
        min_capacity: int = 0,
        available_only: bool = False,
    ) -> list[Facility]:
        """Search for facilities with filters."""
        results = list(self._facilities.values())
        if campus:
            results = [f for f in results if f.campus == campus]
        if facility_type:
            results = [f for f in results if f.facility_type == facility_type]
        if min_capacity > 0:
            results = [f for f in results if f.capacity >= min_capacity]
        if available_only:
            results = [
                f for f in results
                if f.booking_status == BookingStatus.AVAILABLE
            ]
        return results

    def book_facility(
        self, facility_id: str, booked_by: str
    ) -> dict[str, Any]:
        """Book a facility (integrates with Teams Room resource)."""
        facility = self._facilities.get(facility_id)
        if not facility:
            return {"status": "error", "message": "Facility not found"}
        if facility.booking_status != BookingStatus.AVAILABLE:
            return {"status": "error", "message": "Facility not available"}

        facility.booking_status = BookingStatus.BOOKED
        return {
            "status": "success",
            "facility_id": facility_id,
            "booked_by": booked_by,
            "teams_room_id": facility.teams_room_id,
        }

    # ── Staff Directory ──────────────────────────────────────────────

    def register_staff(self, staff: StaffMember) -> StaffMember:
        """Register a staff member."""
        self._staff[staff.staff_id] = staff
        return staff

    def find_staff(
        self,
        role_type: str | None = None,
        faculty: str | None = None,
        department: str | None = None,
    ) -> list[StaffMember]:
        """Search staff directory."""
        results = list(self._staff.values())
        if role_type:
            results = [s for s in results if s.role_type == role_type]
        if faculty:
            results = [
                s for s in results
                if s.faculty.lower() == faculty.lower()
            ]
        if department:
            results = [
                s for s in results
                if s.department.lower() == department.lower()
            ]
        return results

    # ── Service Requests (AI-Assisted) ───────────────────────────────

    def create_service_request(
        self, request: ServiceRequest
    ) -> ServiceRequest:
        """Create a service request with AI-suggested resolution."""
        self._request_counter += 1
        request.request_id = f"SR-{self._request_counter:06d}"

        # AI-assisted triage and suggestion (placeholder for production)
        request.ai_suggested_resolution = self._ai_triage(request)

        self._service_requests[request.request_id] = request
        return request

    def _ai_triage(self, request: ServiceRequest) -> str:
        """AI-assisted triage and resolution suggestion."""
        # Alpha: keyword-based routing
        # Production: Azure AI Foundry model inference
        suggestions = {
            "it_support": "IT Services can assist. Check self-service portal first.",
            "facility": "Facility request routed to campus operations team.",
            "hr": "HR request logged. Contact People & Culture for urgent matters.",
            "finance": "Finance request logged. Check financial portal for status.",
        }
        return suggestions.get(request.service_type, "Request logged for review.")

    def get_campus_dashboard(
        self, campus: CampusLocation | None = None
    ) -> dict[str, Any]:
        """Get campus operations dashboard data."""
        facilities = self.find_facilities(campus=campus) if campus else list(self._facilities.values())
        staff = list(self._staff.values())

        return {
            "campus": campus.value if campus else "all",
            "total_facilities": len(facilities),
            "available_facilities": len(
                [f for f in facilities if f.booking_status == BookingStatus.AVAILABLE]
            ),
            "total_staff": len(staff),
            "academic_staff": len([s for s in staff if s.role_type == "academic"]),
            "professional_staff": len([s for s in staff if s.role_type == "professional"]),
            "open_service_requests": len(
                [r for r in self._service_requests.values() if r.status == "open"]
            ),
        }
