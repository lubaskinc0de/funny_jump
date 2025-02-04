import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

from funny_jump.game.button import Button


class ButtonManager:
    __slots__ = (
        "height",
        "ui_manager",
        "width",
    )

    def __init__(
        self,
        *,
        width: int,
        height: int,
        ui_manager: UIManager,
    ) -> None:
        self.width = width
        self.height = height
        self.ui_manager = ui_manager

    def create_button_menu(
        self,
        buttons: list[Button],
        size: float = 1.0,
    ) -> dict[UIButton, str]:
        menu_buttons: dict[UIButton, str] = {}

        centered_button_index: int | None = None

        button_width = int((self.width // 3) * size)
        button_height = int((self.height // 10) * size)

        if len(buttons) % 2 != 0:
            centered_button_index = len(buttons) // 2

        screen_center = (self.height // 2, self.width // 2)

        button_x = screen_center[1] - button_width // 2
        if centered_button_index is not None:
            button_y = screen_center[0] - int(button_height * (centered_button_index + 0.5))
        else:
            button_y = screen_center[0] - int(button_height * (len(buttons) // 2))

        for button in buttons:
            button.left_top_x = button_x
            button.left_top_y = button_y
            button.width = button_width
            button.height = button_height

            named_ui_button = self.create_button(button)

            menu_buttons[named_ui_button[0]] = named_ui_button[1]

            button_y += button_height

        return menu_buttons

    def create_button(self, button: Button) -> tuple[UIButton, str]:
        ui_button = UIButton(
            relative_rect=pygame.Rect(
                (button.left_top_x, button.left_top_y),
                (button.width, button.height),
            ),
            text=button.text,
            manager=self.ui_manager,
        )

        ui_button.colours["normal_bg"] = pygame.Color(button.color)
        ui_button.colours["hovered_bg"] = pygame.Color(button.hovered_color)
        ui_button.colours["active_bg"] = pygame.Color(button.active_color)
        ui_button.colours["hovered_text"] = pygame.Color("Black")
        # Библиотека содержит неаннотированную функцию, на что ругается mypy
        ui_button.rebuild()  # type: ignore

        return (ui_button, button.name)
