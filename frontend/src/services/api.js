// Use relative URLs to leverage Vite's proxy configuration
// The proxy will forward /api requests to the backend server
const API_URL = '';

// Transform backend data to match frontend component expectations
const transformStudentData = (data) => {
  return {
    // Basic Info
    rollNo: data.roll_no || data.student_id,
    name: data.name,
    course: data.course,
    year: data.year,
    
    // Academic Performance
    attendance: data.attendance_percentage || 0,
    currentCGPA: data.cgpa_current || 0,
    previousCGPA: data.cgpa_previous || 0,
    assignmentsSubmitted: `${data.assignments_submitted || 0} out of ${data.assignments_total || 10}`,
    
    // Engagement
    libraryVisits: data.library_visits_monthly 
      ? `${data.library_visits_monthly} visits/month`
      : '0 visits in 2 months',
    lastLMSLogin: data.lms_last_login_days !== undefined
      ? data.lms_last_login_days === 0 
        ? 'Today'
        : `${data.lms_last_login_days} days ago`
      : 'Unknown',
    extracurricular: data.extracurricular_participation
      ? 'Active participation'
      : 'No participation',
    
    // Financial & Status
    feeStatus: data.tuition_fees_up_to_date ? 'Paid' : 'Pending',
    counselorVisits: data.counselor_visits || '0',
    
    // Profile fields
    gender: data.gender,
    familyIncome: data.family_income_formatted || data.family_income,
    parentEducation: data.parent_education,
    distanceFromCollege: data.distance_from_college ? `${data.distance_from_college} km` : 'N/A',
    accommodation: data.hostel_day_scholar || 'N/A',
    scholarshipHolder: data.scholarship_holder,
    
    // Keep original data for reference
    _raw: data
  };
};

export const getStudentData = async (rollNo) => {
  try {
    const response = await fetch(`${API_URL}/api/student/${rollNo}`);
    if (!response.ok) {
      throw new Error('Student not found');
    }
    const rawData = await response.json();
    return transformStudentData(rawData);
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
    const data = await response.json();
    
    // Transform snake_case to camelCase for frontend
    return {
      error: data.error,
      studentInfo: data.student_info,
      riskLevel: data.risk_level,
      riskLevelInfo: data.risk_level_info,
      riskPercentage: data.risk_percentage,
      riskFactors: data.risk_factors || [],
      recommendations: data.recommendations || [],
      predictionDetails: data.prediction_details
    };
  } catch (error) {
    throw error;
  }
};

export const getTrendData = async (rollNo) => {
  try {
    const response = await fetch(`${API_URL}/api/trends/${rollNo}`);
    if (!response.ok) {
      if (response.status === 404) {
        return { has_data: false, data: null };
      }
      throw new Error('Failed to fetch trend data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching trend data:', error);
    return { has_data: false, data: null };
  }
};

export const getTrendAnalysis = async (rollNo) => {
  try {
    const response = await fetch(`${API_URL}/api/trends/${rollNo}/analysis`);
    if (!response.ok) {
      throw new Error('Failed to fetch trend analysis');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching trend analysis:', error);
    return null;
  }
};

// ============================================================================
// INTERVENTION API
// ============================================================================

export const createIntervention = async (interventionData) => {
  try {
    const response = await fetch(`${API_URL}/api/interventions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(interventionData),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to create intervention');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const getStudentInterventions = async (studentId) => {
  try {
    const response = await fetch(`${API_URL}/api/interventions/student/${studentId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch interventions');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching interventions:', error);
    throw error;
  }
};

export const updateIntervention = async (interventionId, updates) => {
  try {
    const response = await fetch(`${API_URL}/api/interventions/${interventionId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update intervention');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const deleteIntervention = async (interventionId) => {
  try {
    const response = await fetch(`${API_URL}/api/interventions/${interventionId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to delete intervention');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const markAsContacted = async (studentId, contactedBy, notes = '') => {
  try {
    const response = await fetch(`${API_URL}/api/interventions/mark-contacted`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        student_id: studentId,
        contacted_by: contactedBy,
        notes: notes,
      }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to mark as contacted');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const getInterventionStatistics = async (studentId) => {
  try {
    const response = await fetch(`${API_URL}/api/interventions/statistics/${studentId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch statistics');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching statistics:', error);
    return null;
  }
};
