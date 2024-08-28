def undo_last_action(app):
    if app.undo_stack:
        last_action = app.undo_stack.pop()
        # 이전 동작을 취소하는 로직 구현
        # 예를 들어, 아이템 추가/삭제에 따른 되돌리기 동작
        # app.treeview_operations.restore_last_action(last_action)
    else:
        print("Undo stack is empty.")
