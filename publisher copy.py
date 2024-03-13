import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import json
import ssl
import auth_values
import xmlrpc.client

if __name__ == '__main__':
    # Connect to the Odoo server
    common = xmlrpc.client.ServerProxy(f'{auth_values.odoo_url}/xmlrpc/2/common')
    uid = common.authenticate(auth_values.db, auth_values.username, auth_values.password, {})

    # Create a connection to the models
    models = xmlrpc.client.ServerProxy(f'{auth_values.odoo_url}/xmlrpc/2/object')

    # Search for sales orders and fetch data
    sales_orders = models.execute_kw(
        auth_values.db,
        uid,
        auth_values.password,
        'sale.order',
        'search_read',
        [[]],  # Domain (empty to retrieve all records)
        {'fields': ['name', 'partner_id']}  # Fields to fetch
    )

    # Print fetched sales orders
    for order in sales_orders:
        print(f"Order ID: {order['id']}, Order Name: {order['name']}, Customer ID: {order['partner_id']}")

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    auth = {'username': 'admin', 'password': 'Admin12345'}

    # Publish each sales order to the MQTT topic
    for order in sales_orders:
        order_data = {
            'id': order['id'],
            'name': order['name'],
            'customer_id': order['partner_id'][0],  # Assuming partner_id is a many2one field
            # Add other fields as needed
        }
        topic = 'sales_orders'
        payload = json.dumps(order_data)

        publish.single(topic, payload, hostname='0ef562581d144a8da051382a90237387.s1.eu.hivemq.cloud', port=8883, auth=auth, tls=ssl_context, protocol=paho.MQTTv31)
