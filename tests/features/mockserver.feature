Feature: [MOCKSERVER]Mock server return mocked code as requested using requests
    Testing different modes to request mocked codes.
    To complete test, try other methods

Scenario Outline: Ask different codes inside request using different methods
    Given Using "http://localhost:8080" as endpoint
    And Working with "mockserver" mode
    And Load "utils/bodyTest.json" body as template request
    When Using <method> method to ask <code> as mocked code
    Then I get the requested code

    Examples: Post method
        | method    | code  |
        | POST      | 200   |
        | POST      | 300   |
        | POST      | 305   |
        | POST      | 400   |
        | POST      | 404   |
        | POST      | 402   |
        | POST      | 500   |
        | POST      | 501   |