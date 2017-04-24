try:
    import pushbullet
    is_work = True
except ImportError:
    print('pushbullet module not installed')
    is_work = False


def init(api_key: str) -> None:
    global pushobj
    pushobj = pushbullet.Pushbullet(api_key)


def send(title: str, body: str) -> None:
    push = pushobj.push_note(title, body)

#print(pb.get_pushes())
