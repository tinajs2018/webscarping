import jinja2
env= jinja2.environment()
template=env.from_string("hello{{name}}")

template.render(name="Tina")