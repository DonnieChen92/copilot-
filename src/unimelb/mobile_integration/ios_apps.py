"""
iOS Mobile App Integration Layer
==================================
Integrates the UniMelb AI Platform with two official iOS apps:

1. UniMelb Official App — Apple ID: 904152776
   Student portal, timetables, campus maps, notifications

2. MyMBS App — Apple ID: 1095799806
   Melbourne Business School: events, networking, MBS-specific content

Both apps authenticate via Microsoft Entra ID (SAML 2.0 / OIDC)
and receive push notifications via Apple Push Notification Service (APNS).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class iOSApp(Enum):
    """Registered iOS applications."""

    UNIMELB_OFFICIAL = "904152776"
    MYMBS = "1095799806"


class NotificationType(Enum):
    """Push notification categories."""

    AI_RESPONSE_READY = "ai_response_ready"
    COURSE_UPDATE = "course_update"
    ASSIGNMENT_DUE = "assignment_due"
    GRADE_PUBLISHED = "grade_published"
    CAMPUS_ALERT = "campus_alert"
    PROPERTY_MAINTENANCE = "property_maintenance"
    LIFE_CHALLENGE_SUPPORT = "life_challenge_support"
    MIGRATION_STATUS = "migration_status"
    MBS_EVENT = "mbs_event"
    VERIFICATION_COMPLETE = "verification_complete"


@dataclass
class AppUser:
    """A user registered on one or both iOS apps."""

    user_id: str
    email: str
    display_name: str
    apps_installed: list[iOSApp] = field(default_factory=list)
    device_tokens: dict[str, str] = field(default_factory=dict)
    # app_id → APNS device token
    entra_id: str = ""
    push_enabled: bool = True
    notification_preferences: dict[str, bool] = field(default_factory=dict)


@dataclass
class PushNotification:
    """A push notification to be sent via APNS."""

    notification_id: str
    target_app: iOSApp
    target_user_id: str
    notification_type: NotificationType
    title: str
    body: str
    data: dict[str, Any] = field(default_factory=dict)
    sent_at: datetime | None = None
    delivered: bool = False
    read: bool = False


@dataclass
class AppEndpoint:
    """An API endpoint exposed to the iOS apps."""

    path: str
    method: str  # GET | POST | PUT | DELETE
    description: str
    auth_required: bool = True
    app_scope: list[iOSApp] = field(default_factory=list)  # empty = all apps


class iOSAppIntegrationLayer:
    """
    Integration layer between UniMelb AI Platform and iOS apps.

    Provides:
    - SSO authentication via Entra ID
    - APNS push notification delivery
    - REST API endpoints for app features
    - Deep linking between apps and platform
    """

    # API endpoints exposed to iOS apps
    API_ENDPOINTS = [
        # Authentication
        AppEndpoint(
            path="/api/v1/auth/sso",
            method="POST",
            description="SSO login via Microsoft Entra ID (SAML 2.0 / OIDC)",
        ),
        AppEndpoint(
            path="/api/v1/auth/refresh",
            method="POST",
            description="Refresh authentication token",
        ),
        # AI Chat
        AppEndpoint(
            path="/api/v1/ai/chat",
            method="POST",
            description="Send query to UniMelb AI Copilot",
        ),
        AppEndpoint(
            path="/api/v1/ai/chat/history",
            method="GET",
            description="Get chat history for current session",
        ),
        AppEndpoint(
            path="/api/v1/ai/verification/{query_id}",
            method="GET",
            description="Get verification status for an AI response",
        ),
        # Courses & Academics
        AppEndpoint(
            path="/api/v1/courses",
            method="GET",
            description="List enrolled courses (Teams-based)",
        ),
        AppEndpoint(
            path="/api/v1/courses/{course_id}/assignments",
            method="GET",
            description="List assignments for a course",
        ),
        AppEndpoint(
            path="/api/v1/courses/{course_id}/grades",
            method="GET",
            description="Get grades for a course",
        ),
        # Campus
        AppEndpoint(
            path="/api/v1/campus/maps",
            method="GET",
            description="Get campus maps and navigation",
            app_scope=[iOSApp.UNIMELB_OFFICIAL],
        ),
        AppEndpoint(
            path="/api/v1/campus/timetable",
            method="GET",
            description="Get student timetable",
            app_scope=[iOSApp.UNIMELB_OFFICIAL],
        ),
        AppEndpoint(
            path="/api/v1/campus/alerts",
            method="GET",
            description="Get campus safety alerts",
            app_scope=[iOSApp.UNIMELB_OFFICIAL],
        ),
        # MBS-specific
        AppEndpoint(
            path="/api/v1/mbs/events",
            method="GET",
            description="Melbourne Business School events",
            app_scope=[iOSApp.MYMBS],
        ),
        AppEndpoint(
            path="/api/v1/mbs/network",
            method="GET",
            description="MBS networking directory",
            app_scope=[iOSApp.MYMBS],
        ),
        # Life Challenge Programme
        AppEndpoint(
            path="/api/v1/life-challenge/status",
            method="GET",
            description="Get Life Challenge Programme status",
        ),
        AppEndpoint(
            path="/api/v1/life-challenge/support",
            method="GET",
            description="Get available support resources",
        ),
        # Property (staff/tenants only)
        AppEndpoint(
            path="/api/v1/property/maintenance",
            method="POST",
            description="Submit maintenance request",
            auth_required=True,
        ),
        # Notifications
        AppEndpoint(
            path="/api/v1/notifications",
            method="GET",
            description="Get notification history",
        ),
        AppEndpoint(
            path="/api/v1/notifications/preferences",
            method="PUT",
            description="Update notification preferences",
        ),
    ]

    def __init__(
        self,
        apns_key_id: str = "",
        apns_team_id: str = "",
        apns_bundle_ids: dict[str, str] | None = None,
    ):
        self.apns_key_id = apns_key_id
        self.apns_team_id = apns_team_id
        self.apns_bundle_ids = apns_bundle_ids or {
            iOSApp.UNIMELB_OFFICIAL.value: "au.edu.unimelb.app",
            iOSApp.MYMBS.value: "au.edu.unimelb.mbs",
        }
        self._users: dict[str, AppUser] = {}
        self._notifications: list[PushNotification] = []
        self._notification_counter = 0

    # ── User Management ──────────────────────────────────────────────

    def register_device(
        self,
        user_id: str,
        app: iOSApp,
        device_token: str,
        email: str = "",
        display_name: str = "",
    ) -> AppUser:
        """Register a user's device for an iOS app."""
        user = self._users.get(user_id)
        if not user:
            user = AppUser(
                user_id=user_id,
                email=email,
                display_name=display_name,
            )
            self._users[user_id] = user

        if app not in user.apps_installed:
            user.apps_installed.append(app)
        user.device_tokens[app.value] = device_token
        return user

    def get_user(self, user_id: str) -> AppUser | None:
        """Get an app user."""
        return self._users.get(user_id)

    # ── Push Notifications ───────────────────────────────────────────

    def send_notification(
        self,
        target_app: iOSApp,
        target_user_id: str,
        notification_type: NotificationType,
        title: str,
        body: str,
        data: dict[str, Any] | None = None,
    ) -> PushNotification | None:
        """
        Send a push notification to a user's iOS device via APNS.

        Respects user notification preferences.
        """
        user = self._users.get(target_user_id)
        if not user:
            return None

        # Check preferences
        pref_key = notification_type.value
        if not user.notification_preferences.get(pref_key, True):
            return None

        # Check if user has the app installed
        if target_app not in user.apps_installed:
            return None

        self._notification_counter += 1
        notification = PushNotification(
            notification_id=f"PN-{self._notification_counter:08d}",
            target_app=target_app,
            target_user_id=target_user_id,
            notification_type=notification_type,
            title=title,
            body=body,
            data=data or {},
            sent_at=datetime.now(),
        )
        self._notifications.append(notification)

        # In production: call APNS with device_token
        # Alpha: simulate delivery
        notification.delivered = True

        return notification

    def send_ai_response_notification(
        self,
        user_id: str,
        query_preview: str,
        confidence_score: float,
    ) -> PushNotification | None:
        """Send notification that an AI response is ready with verification."""
        confidence_text = (
            "High confidence"
            if confidence_score >= 0.8
            else "Partially verified"
            if confidence_score >= 0.6
            else "Manual review recommended"
        )

        return self.send_notification(
            target_app=iOSApp.UNIMELB_OFFICIAL,
            target_user_id=user_id,
            notification_type=NotificationType.AI_RESPONSE_READY,
            title="AI Response Ready",
            body=f"{query_preview[:80]}... [{confidence_text}]",
            data={
                "confidence_score": confidence_score,
                "action": "open_ai_chat",
            },
        )

    # ── API Endpoint Registry ────────────────────────────────────────

    def get_api_endpoints(
        self, app: iOSApp | None = None
    ) -> list[AppEndpoint]:
        """Get API endpoints, optionally filtered by app."""
        if not app:
            return self.API_ENDPOINTS
        return [
            e
            for e in self.API_ENDPOINTS
            if not e.app_scope or app in e.app_scope
        ]

    def get_api_spec(self) -> dict[str, Any]:
        """Generate OpenAPI-compatible spec summary for iOS apps."""
        endpoints = {}
        for ep in self.API_ENDPOINTS:
            endpoints[ep.path] = {
                "method": ep.method,
                "description": ep.description,
                "auth_required": ep.auth_required,
                "app_scope": [a.value for a in ep.app_scope] or ["all"],
            }
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "UniMelb AI Platform — iOS API",
                "version": "1.0.0-alpha",
                "description": (
                    "REST API for UniMelb Official App (904152776) "
                    "and MyMBS App (1095799806)"
                ),
            },
            "servers": [
                {"url": "https://api.ai.unimelb.edu.au", "description": "Production"},
                {"url": "https://api-staging.ai.unimelb.edu.au", "description": "Staging"},
            ],
            "paths": endpoints,
            "security": [{"entra_id_sso": []}],
        }
