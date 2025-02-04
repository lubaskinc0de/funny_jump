import pygame


class LogoFontMissingError(Exception):
    ...

class TextFontMissingError(Exception):
    ...


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
        screen_width: int,
        screen: pygame.Surface,
        text_coord: int = 50,
        text_font: pygame.font.Font | None = None,
        logo_font: pygame.font.Font | None = None,
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
        if not self.logo_font:
            raise LogoFontMissingError

        string_rendered = self.logo_font.render(
            text,
            antialias=True,
            color=pygame.Color(color),
            )
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
        font: pygame.Font | None = None
    ) -> None:
        if not self.text_font and not font:
            raise TextFontMissingError
        
        usable_font = self.text_font if not font else font
        
        if has_vertical_indent:
            self.text_coord += usable_font.get_height()

        space_width = usable_font.render(
            " ",
            antialias=True,
            color=pygame.Color(color),
            ).get_width()
        splited_text_with_length: list[list[str, int]] = [["", 0]]  # type: ignore
        counter = 0

        for _word in text.split():
            word = " " + _word
            string_rendered = usable_font.render(
                word,
                antialias=True,
                color=pygame.Color(color),
                )
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
            string_rendered = usable_font.render(
                text_line,
                antialias=True,
                color=pygame.Color(color),
                )
            intro_rect = string_rendered.get_rect()
            self.text_coord += 10
            intro_rect.top = self.text_coord
            intro_rect.x = indent
            self.text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
