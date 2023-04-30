Feature: Mock server return mocked code as requested


Scenario Outline: Ask different codes using different methods
    Given Using "http://localhost:8080" as endpoint
    And Working with "mockurl" mode
    # When Using <method> method
    # And Ask <code> as mocked code
    When Using <method> method to Ask <code> as mocked code
    Then I get the requested code
    
    Examples: Get method
        | method    | code |
        | GET		| 200  |
        | GET		| 300  |
        | GET		| 305  |
        | GET		| 400  |
        | GET		| 404  |
        | GET		| 402  |
        | GET		| 500  |
        | GET		| 501  |
    
    Examples: Post method
        | method    | code |
        | POST		| 200  |
        | POST		| 300  |
        | POST		| 305  |
        | POST		| 400  |
        | POST		| 404  |
        | POST		| 402  |
        | POST		| 500  |
        | POST		| 501  |