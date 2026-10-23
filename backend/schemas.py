from pydantic import BaseModel, Field
from typing import Optional

class OrderPredictionInput(BaseModel):
    Quantity: int = Field(..., ge=1, le=100, description="Order quantity")
    Unit_Price_INR: float = Field(..., gt=0, description="Unit price in INR")
    Discount: float = Field(..., ge=0.0, le=1.0, description="Discount rate between 0.0 and 1.0")
    Category: str = Field(..., example="Electronics")
    Subcategory: str = Field(..., example="Mobiles")
    Region: str = Field(..., example="North")
    Segment: str = Field(..., example="Consumer")
    Channel: str = Field(..., example="Online")
    Payment_Method: str = Field(..., example="Credit Card")
    Order_Month: int = Field(..., ge=1, le=12, description="Month of order (1-12)")
    Order_DayOfWeek: int = Field(..., ge=0, le=6, description="Day of week (0=Mon, 6=Sun)")

class RegressionResponse(BaseModel):
    predicted_profit_inr: float
    currency: str = "INR"
    status: str = "success"

class ClassificationResponse(BaseModel):
    predicted_returned: str
    return_probability: float
    keep_probability: float
    status: str = "success"

class HealthResponse(BaseModel):
    status: str
    regression_model_loaded: bool
    classification_model_loaded: bool