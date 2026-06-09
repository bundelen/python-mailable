from python_mailable.mailable import Mailable


class OrderShipped(Mailable):
    def build(self):
        return self


def test_it_can_set_the_recipient():
    email_address = "john.doe@example.net"

    email = OrderShipped().build().to(email_address)

    assert email._to_email == email_address


def test_it_can_set_one_cc_email_address():
    cc_email_address = ["john.doe-bcc@example.net"]

    email = OrderShipped().build().cc(*cc_email_address)

    assert email._to_cc == cc_email_address


def test_it_can_set_multiple_cc_email_addresses():
    cc_email_addresses = ["john.doe-bcc@example.net", "doe.john@example.net"]

    email = OrderShipped().build().cc(*cc_email_addresses)

    assert email._to_cc == cc_email_addresses


def test_it_can_set_one_bcc_email_address():
    bcc_email_address = ["john.doe-bcc@example.net"]

    email = OrderShipped().build().bcc(*bcc_email_address)

    assert email._to_bcc == bcc_email_address


def test_it_can_set_multiple_bcc_email_addresses():
    bcc_email_addresses = ["john.doe-bcc@example.net", "doe.john@example.net"]

    email = OrderShipped().build().bcc(*bcc_email_addresses)

    assert email._to_bcc == bcc_email_addresses


def test_it_can_set_the_subject():
    subject = "Order has been shipped"

    email = OrderShipped().build().subject(subject)

    assert email._subject_line == subject


def test_it_can_set_the_template_path():
    template_path = "emails/order_shipped.html"

    email = OrderShipped().build().template(template_path)

    assert email._template_path == template_path


def test_it_can_set_the_text_template_path():
    text_template_path = "emails/order_shipped.txt"

    email = OrderShipped().build().text_template(text_template_path)

    assert email._text_template_path == text_template_path


def test_it_can_set_the_context():
    context = {"order_id": 42, "customer": "John Doe"}

    email = OrderShipped().build().with_context(context)

    assert email._context == context


def test_it_can_extend_the_context():
    initial_context = {"order_id": 42}
    additional_context = {"customer": "John Doe"}

    email = (
        OrderShipped()
        .build()
        .with_context(initial_context)
        .with_context(additional_context)
    )

    assert email._context == {"order_id": 42, "customer": "John Doe"}


def test_it_can_attach_one_file():
    file_path = "invoices/order_42.pdf"

    email = OrderShipped().build().attach(file_path)

    assert email._attachments == [file_path]


def test_it_can_attach_multiple_files():
    files = ["invoice.pdf", "package.pdf"]

    email = OrderShipped().build().attach(files[0]).attach(files[1])

    assert email._attachments == files


def test_render_returns_none_without_template():
    email = OrderShipped().build()

    assert email.render() is None


def test_render_returns_none_without_text_template():
    email = OrderShipped().build()

    assert email.render(as_text=True) is None


def test_render_as_text_returns_none_without_text_template():
    email = OrderShipped().build()

    assert email.render_as_text() is None
