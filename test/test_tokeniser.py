from joml.tokeniser import Token, TokenType, tokenise


def test_simple():
    string = "From heathrow on 2020-01-01 to gatwick by plane"

    tokens = tokenise(string)

    assert len(tokens) == 8

    assert tokens[0] == Token(TokenType.KEYWORD, "from")
    assert tokens[1] == Token(TokenType.STRING, "heathrow")
    assert tokens[2] == Token(TokenType.KEYWORD, "on")
    assert tokens[3] == Token(TokenType.DATE, "2020-01-01")
    assert tokens[4] == Token(TokenType.KEYWORD, "to")
    assert tokens[5] == Token(TokenType.STRING, "gatwick")
    assert tokens[6] == Token(TokenType.KEYWORD, "by")
    assert tokens[7] == Token(TokenType.STRING, "plane")


def test_time():
    string = "From heathrow on 2020-01-01 at 09:30 to gatwick by plane"

    tokens = tokenise(string)

    assert len(tokens) == 10

    assert tokens[0] == Token(TokenType.KEYWORD, "from")
    assert tokens[1] == Token(TokenType.STRING, "heathrow")
    assert tokens[2] == Token(TokenType.KEYWORD, "on")
    assert tokens[3] == Token(TokenType.DATE, "2020-01-01")
    assert tokens[4] == Token(TokenType.KEYWORD, "at")
    assert tokens[5] == Token(TokenType.TIME, "09:30")
    assert tokens[6] == Token(TokenType.KEYWORD, "to")
    assert tokens[7] == Token(TokenType.STRING, "gatwick")
    assert tokens[8] == Token(TokenType.KEYWORD, "by")
    assert tokens[9] == Token(TokenType.STRING, "plane")
