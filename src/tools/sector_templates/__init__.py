"""
Sector-specific DPR templates.
"""
from .water_supply_dpr import WaterSupplyDPRTemplate
from .solid_waste_dpr import SolidWasteDPRTemplate
from .urban_transport_dpr import UrbanTransportDPRTemplate
from .streetlight_dpr import StreetlightDPRTemplate

__all__ = [
    "WaterSupplyDPRTemplate",
    "SolidWasteDPRTemplate",
    "UrbanTransportDPRTemplate",
    "StreetlightDPRTemplate"
]


