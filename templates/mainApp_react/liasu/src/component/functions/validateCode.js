import getCookie from "./getCookie";
const validateCode = async (code, email, username, password) => {
  try {
    console.log(code, email, username, password);
    const response = await fetch(`/api/validate-code/`, {
      method: 'POST', // GET request
      headers: {
        'Content-Type': 'application/json', // Let the backend know you're sending JSON data
        'X-CSRFToken': getCookie("csrftoken"),

      },
        body: JSON.stringify({ code, email, username, password  }), // Send the ID in the request body
    });

    if (!response.ok) {
      // If HTTP response is not OK (status is not 2xx)
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json(); // Parse JSON response
    return data;
  } catch (error) {
    // Handle network or other errors
    console.error('Error during validation request:', error.message);
  }
  return false; // Return false if validation fails or an error occurs
};

export default validateCode;