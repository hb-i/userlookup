from flask import *

app = Flask(__name__)

@app.route('/')
def customer():
    return render_template('userform.html')

@app.route('/success', methods=['POST', 'GET'])
def print_data():
    if request.method == 'POST':
        result = request.form
        fullname = result['firstname'] + ' ' + result['lastname'] # Format first and last name to lookup displayname attriubute
        from ldap3 import Server, Connection

        server = Server('DomainController.example.com', port=636, use_ssl=True)
        conn = Connection(server, 'CN=LDAPUser,CN=Users,DC=example,DC=com', 'PasswordForLDAPUser', auto_bind=True)
        # print(conn) # Used to test if the connections was successful (True/False)

        # Search user using the displayname attribute and output the samaccountname attribute it finds
        query = '(&(objectclass=user)(displayName=' + fullname + '))'
        conn.search('DC=example,DC=com', query,
                    attributes=['samaccountname', 'mail'])

        # Select the first entry in case of multiple results
        entry = conn.entries[0]
        username = entry.sAMAccountName
        email = entry.mail

        return render_template("result_data.html", result=result, username=username, email=email)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')