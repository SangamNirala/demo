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
    
    // Additional fields
    gender: data.gender,
    hostelDayScholar: data.hostel_day_scholar,
    familyIncome: data.family_income_formatted || data.family_income,
    parentEducation: data.parent_education,
    scholarshipHolder: data.scholarship_holder,
    distance: data.distance_from_college
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
    return await response.json();
  } catch (error) {
    throw error;
  }
};
