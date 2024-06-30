NAME = program
CPPFLAGS = -Wall -Wextra -Werror -std=c++98
SRC = MyClass.cpp main.cpp

all: $(SRC)
	c++ $(CPPFLAGS) $(SRC) -o $(NAME)

clean:

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
