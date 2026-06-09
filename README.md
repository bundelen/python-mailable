# Python Mailable

**Python Mailable** is an email builder for Python, inspired by Laravel's Mailable class. It provides a clean and reusable structure for defining, composing, and rendering emails with rich context and templates.

> [!IMPORTANT]  
> We currently only support _rendering_ emails, not sending them.
>
> This package helps you build and render email content using templates, but you need to handle email sending yourself with your own SMTP client or email delivery service.

## Features

- Define email classes with subjects, recipients, and templates
- Render HTML and plain-text versions from separate Jinja2 templates
- Pass context to templates for dynamic rendering
- Attach files easily
- Designed for clarity, testability, and reusability

## Usage

### Creating a Mailable

Subclass `Mailable` and implement the `build()` method. Use the fluent API to configure the email.

```python
from dataclasses import dataclass
from python_mailable import Mailable

@dataclass
class OrderShipped(Mailable):
    user: User

    def build(self):
        return (
            self.to(self.user.email)
                .subject("Your order has shipped!")
                .template("emails/order_shipped.html.j2")
                .with_context({"user": self.user})
        )
```

### Rendering HTML

```python
email = OrderShipped(user).build()
html = email.render()
```

### Rendering a plain-text version

Provide a separate plain-text template alongside the HTML template using `text_template()`.

```python
@dataclass
class OrderShipped(Mailable):
    user: User

    def build(self):
        return (
            self.to(self.user.email)
                .subject("Your order has shipped!")
                .template("emails/order_shipped.html.j2")
                .text_template("emails/order_shipped.txt.j2")
                .with_context({"user": self.user})
        )
```

Then render either version:

```python
email = OrderShipped(user).build()

html = email.render()
text = email.render_as_text()
```

`render_as_text()` returns `None` when no text template has been set. `render()` returns `None` when no HTML template has been set.

### Sending the email

Pass the rendered content into your own delivery system:

```python
email = OrderShipped(user).build()

your_mail_client.send(
    to=email._to_email,
    subject=email._subject_line,
    html=email.render(),
    text=email.render_as_text(),
)
```
