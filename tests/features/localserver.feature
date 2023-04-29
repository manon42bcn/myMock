Feature: Mock server is running at local env

    Feature Description: Mock server running on local environment

Scenario: Asking different mock codes using mockurl mod
    Given Local myMockServer running
    And Using "localhost:80" as endpoint
    And Working with "mockurl" mode
    When I ask a "305" codes
    Then I get the requested code