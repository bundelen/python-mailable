from dataclasses import dataclass

from python_mailable.mailable import Mailable


@dataclass
class OrderShipped(Mailable):
    def build(self):
        context = {
            "customer_name": "John Doe",
            "order_id": "123456",
            "shipping_address": "Vijzelstraat 32, Amsterdam, The Netherlands",
            "carrier": "UPS",
            "tracking_number": "1Z999AA10123456784",
        }

        return (
            self.to("john.doe@example.net")
            .subject("Your order has shipped!")
            .template("/tests/integration/templates/order_shipped.html.j2")
            .with_context(context)
        )


@dataclass
class OrderCancelled(Mailable):
    def build(self):
        context = {
            "customer_name": "John Doe",
            "order_id": "789012",
            "cancellation_reason": "Item out of stock",
            "refund_amount": "€49.99",
            "refund_method": "Original payment method",
        }

        return (
            self.to("john.doe@example.net")
            .subject("Your order has been cancelled")
            .text_template("/tests/integration/templates/order_cancelled.txt.j2")
            .with_context(context)
        )


def test_order_shipped_renders_successfully():
    email = OrderShipped().build()
    html = email.render()

    assert "John Doe" in html
    assert "123456" in html
    assert "Vijzelstraat 32, Amsterdam, The Netherlands" in html
    assert "UPS" in html
    assert "1Z999AA10123456784" in html
    assert "Your order has shipped!" in html

    assert "<html>" in html
    assert "</html>" in html


def test_render_text_returns_none_without_text_template():
    email = OrderShipped().build()

    assert email.render(as_text=True) is None


def test_order_cancelled_renders_text_successfully():
    email = OrderCancelled().build()
    text = email.render(as_text=True)

    assert "John Doe" in text
    assert "789012" in text
    assert "Item out of stock" in text
    assert "€49.99" in text
    assert "Original payment method" in text
    assert "Your order has been cancelled" in text

    assert "<html>" not in text
    assert "<" not in text
