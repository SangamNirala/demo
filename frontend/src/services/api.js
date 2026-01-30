const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getStudentData = async (rollNo) => {
  try {
    const response = await fetch(`${API_URL}/api/student/${rollNo}`);
    if (!response.ok) {
      throw new Error('Student not found');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const getPrediction = async (rollNo) => {
  try {
    const response = await fetch(`${API_URL}/api/predict/${rollNo}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Prediction failed');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};
