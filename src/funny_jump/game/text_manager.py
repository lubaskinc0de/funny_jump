import pygame


class TextManager:
    __slots__ = (
        "logo_font",
        "screen",
        "screen_width",
        "text_coord",
        "text_font",
    )
    def __init__(
        self,
        text_font: pygame.font.Font,
        logo_font: pygame.font.Font,
        screen_width: int,
        screen: pygame.Surface,
        text_coord: int = 50,
    ) -> None:
        self.text_font = text_font
        self.logo_font = logo_font
        self.screen_width = screen_width
        self.screen = screen
        self.text_coord = text_coord

    def render_as_logo(
        self,
        text: str,
        color: str = "White",
    ) -> None:
        string_rendered = self.logo_font.render(text, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        self.text_coord += 10
        intro_rect.top = self.text_coord
        intro_rect.x = (self.screen_width - string_rendered.get_width()) // 2
        self.text_coord += intro_rect.height
        self.screen.blit(string_rendered, intro_rect)

    def render_as_text(
        self,
        text: str,
        color: str = "White",
        indent: int = 10,
        has_vertical_indent: bool = True,
    ) -> None:
        if has_vertical_indent:
            self.text_coord += self.text_font.get_height()

        space_width = self.text_font.render(" ", 1, pygame.Color(color)).get_width()
        splited_text_with_length: list[list[str, int]] = [["", 0]]  # type: ignore
        counter = 0

        for _word in text.split():
            word = " " + _word
            string_rendered = self.text_font.render(word, 1, pygame.Color(color))
            word_width = string_rendered.get_width()

            if splited_text_with_length[counter][1] + word_width < self.screen_width - indent * 2:
                splited_text_with_length[counter][0] += word
                splited_text_with_length[counter][1] += word_width

                if splited_text_with_length[counter][1] == word_width:
                    splited_text_with_length[counter][1] = word_width - space_width
                    splited_text_with_length[counter][0] = splited_text_with_length[counter][0].lstrip(" ")
            else:
                counter += 1
                splited_text_with_length.append([word.lstrip(" "), word_width - space_width])

        splited_text = [txt[0] for txt in splited_text_with_length]

        for text_line in splited_text:
            string_rendered = self.text_font.render(text_line, 1, pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            self.text_coord += 10
            intro_rect.top = self.text_coord
            intro_rect.x = indent
            self.text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
