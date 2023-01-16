import pynecone as pc
import pandas as pd


nba_data = pd.read_csv(
    "https://media.geeksforgeeks.org/wp-content/uploads/nba.csv"
)

class State(pc.State):
    count: int = 0
    text1: str = "First lv header:"
    text2: str = "Last lv header:"
    
    @pc.var
    def print_text1(self) -> str:
        if self.text1 == "First lv header:":
            return self.text1
        else:
            return "First lv header:" + "  " + self.text1
    @pc.var
    def print_text2(self) -> str:
        if self.text2 == "Last lv header:":
            return self.text2
        else:
            return "Last lv header:" + "  " + self.text2

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1


def mk_table():
    return pc.data_table(
            data=nba_data[["Name", "Team", "Position", "Height", "Salary", "Age"]],
            pagination=True,
            search=True,
            sort=True,
            width="100%")

def index():
    return pc.vstack(
        pc.heading("Building List Parser"),
        pc.container(
            pc.vstack(
                pc.hstack(
                    pc.button(
                        "Decrement",
                        color_scheme="red",
                        border_radius="1em",
                        on_click=State.decrement),
                    pc.heading(State.count, font_size="2em"),
                    pc.button(
                        "Increment",
                        color_scheme="green",
                        border_radius="1em",
                        on_click=State.increment)),
                pc.hstack(
                    pc.vstack(
                        pc.heading(State.print_text1, size="sm"),
                        pc.input(
                            on_blur=State.set_text1,
                            placeholder="Type here...")),
                    pc.vstack(
                        pc.heading(State.print_text2, size="sm"),
                        pc.input(
                            on_blur=State.set_text2,
                            placeholder="Type here...")),
                    ),
                # pc.hstack(
                #     lv_properties_input("first"),
                #     lv_properties_input("first"),
                #     ),
            center_content=True)),
        pc.box(
            mk_table()),
        width="100%")

# def index():
#     return pc.vstack(
#         pc.box(
#             mk_table()),
#         width="100%")

app = pc.App(state=State)
app.add_page(index)
app.compile()