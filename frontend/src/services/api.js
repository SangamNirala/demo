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
    });
    if (!response.ok) {
      throw new Error('Prediction failed');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};
