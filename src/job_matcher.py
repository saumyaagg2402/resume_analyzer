from openai import OpenAI
import os
import json

class JobMatcher:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def calculate_match_score(self, resume_text: str, job_description: str) -> dict:
        analysis_prompt = f"""
        Analyze this resume against the job description with strict accuracy:

        1. ONLY list skills and qualifications that are EXPLICITLY mentioned in the resume
        2. Do not infer or assume skills that aren't directly stated
        3. For each matching skill, include the exact text or evidence from the resume
        4. Educational qualifications should be exactly matched
        
        Format your analysis as JSON:
        {{
            "match_score": <number between 0-100>,
            "matching_skills": [
                {{
                    "skill": "skill name",
                    "evidence": "exact text from resume"
                }}
            ],
            "missing_skills": [
                {{
                    "skill": "required skill",
                    "reason": "why it's considered missing"
                }}
            ],
            "feedback": "detailed feedback with specific examples"
        }}
        
        Job Description:
        {job_description}

        Resume Content:
        {resume_text}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a precise HR analyst. Only match skills that are explicitly stated in the resume. Do not make assumptions about unstated skills."
                    },
                    {
                        "role": "user", 
                        "content": analysis_prompt
                    }
                ],
                temperature=0.3  # Reduced for more consistent outputs
            )

            result = json.loads(response.choices[0].message.content)
            
            # Validate and normalize
            self._validate_result(result)
            
            return result

        except Exception as e:
            print(f"Error processing analysis: {str(e)}")
            return self._get_error_response(str(e))

    def _validate_result(self, result):
        required_fields = ['match_score', 'matching_skills', 'missing_skills', 'feedback']
        if not all(field in result for field in required_fields):
            raise ValueError("Missing required fields in response")
        result['match_score'] = max(0, min(100, float(result['match_score'])))

    def _get_error_response(self, error_msg):
        return {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "feedback": f"Error analyzing resume: {error_msg}"
        }