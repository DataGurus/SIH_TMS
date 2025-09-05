# Tourist Management System (Document and Face Verification)

This project is a Tourist Management System that uses document and face verification for user authentication. It leverages technologies like Flask, Mediapipe, and OpenCV for efficient and secure verification processes.

## Features
- **Document Verification**: Validate user identity using document numbers (e.g., Aadhaar, PAN, Passport).
- **Face Verification**: Extract and compare facial embeddings for authentication.
- **Integration with VigiLocker**: Communicates with a mock DigiLocker API for document validation.
- **High Accuracy**: Uses Mediapipe and scikit-learn for precise facial landmark detection and similarity calculations.

## Technologies Used
- **Flask**: Backend framework for building the API.
- **Mediapipe**: For facial landmark detection.
- **OpenCV**: For image processing.
- **NumPy**: For numerical operations.
- **scikit-learn**: For calculating cosine similarity.
- **Python**: Programming language for the entire project.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd SIH_TMS
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv sih
   source sih/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app2.py
   ```

5. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5002`.

## Project Structure
- `app2.py`: Main Flask application for user verification.
- `face2embed.py`: Handles facial embedding extraction.
- `vigiLocker.py`: Mock DigiLocker API for document validation.
- `templates/`: Contains HTML templates for the web interface.
- `static/`: Contains static files like CSS and JavaScript.
- `requirements.txt`: Lists all the dependencies for the project.

## How It Works
1. **User Input**:
   - The user submits their name, document number, and a photo.
2. **Face Processing**:
   - The photo is processed using Mediapipe to extract facial landmarks.
3. **Embedding Comparison**:
   - The extracted embeddings are compared with stored embeddings to calculate similarity.
4. **Document Validation**:
   - The document number is validated via the VigiLocker API.
5. **Result**:
   - The user is authenticated if both the document and face verification succeed.

## Future Enhancements
- Add support for multiple document types.
- Improve the user interface for better usability.
- Integrate with real-world APIs for document validation.

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.