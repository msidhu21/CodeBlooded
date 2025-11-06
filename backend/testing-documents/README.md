Testing Evidence – Milestone 3:

This folder shows the testing results for **User Story 1: User Registration**.

- All the tests for the **AuthService** worked properly using `pytest`.  
- The screenshot `pytest_results.png` shows the test results.  

What I Tested:
- Registering a new user with a unique email  
- Checking that duplicate emails don’t get registered again  
- Making sure the system catches when info is missing  

All tests passed successfully in the backend environment.

Notees:
- My test file is in `backend/tests/test_auth_service.py`.  
- The code I tested is in `backend/app/services/auth_service.py`.  
- These tests show that the register function works how it should and follows the User Story 1 goals.

