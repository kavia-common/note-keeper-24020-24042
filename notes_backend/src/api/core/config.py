"""
Application configuration and theme definitions for the Notes Backend.

This module centralizes FastAPI app metadata, OpenAPI customization, and future
environment-driven configuration to keep code clean and extensible.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import os


class Theme(BaseModel):
    """Represents the Ocean Professional theme for docs/UI presentation."""
    name: str = Field(default="Ocean Professional", description="Theme name")
    description: str = Field(default="Blue & amber accents", description="Theme summary")
    primary: str = Field(default="#2563EB", description="Primary brand color (blue)")
    secondary: str = Field(default="#F59E0B", description="Secondary accent color (amber)")
    success: str = Field(default="#F59E0B", description="Success color (amber)")
    error: str = Field(default="#EF4444", description="Error color")
    gradient: str = Field(default="from-blue-500/10 to-gray-50", description="Gradient hint")
    background: str = Field(default="#f9fafb", description="Background color")
    surface: str = Field(default="#ffffff", description="Surface color")
    text: str = Field(default="#111827", description="Text color")


class AppConfig(BaseModel):
    """Holds application-level settings and OpenAPI metadata."""
    app_name: str = Field(default="Notes Backend API", description="Human readable app name")
    description: str = Field(
        default=(
            "Modern, modular, and extensible notes management API.\n\n"
            "- Ocean Professional theme (blue with amber accents)\n"
            "- Clean architecture with routers, schemas, and a repository layer\n"
            "- Ready for future integration with a dedicated notes_database service"
        ),
        description="OpenAPI description"
    )
    version: str = Field(default="1.0.0", description="API version")
    theme: Theme = Field(default_factory=Theme, description="Docs/UI theme")

    # Placeholder for future DB connection settings
    database_url: Optional[str] = Field(
        default=None,
        description="Future database URL (provided via env). Not used in mock mode."
    )

    # PUBLIC_INTERFACE
    def openapi_meta(self) -> Dict[str, Any]:
        """Return the base OpenAPI metadata block for FastAPI app creation."""
        return {
            "title": self.app_name,
            "description": self.description,
            "version": self.version,
        }


def load_config() -> AppConfig:
    """
    Load the application configuration from environment variables when available.

    This function prepares the system for future database integration by
    reading values from environment variables if provided.
    """
    return AppConfig(
        app_name=os.getenv("APP_NAME", "Notes Backend API"),
        version=os.getenv("APP_VERSION", "1.0.0"),
        database_url=os.getenv("NOTES_DATABASE_URL"),  # For future use
    )
