
from io import BytesIO
from X2.XDB.xceph import login_ceph


if __name__ == '__main__':

    ldap_username = ''
    ldap_password = ''
    ceph_endpoint = ''

    test_file = './test'

    ceph_conn = login_ceph(ldap_username, ldap_password)

    # ==============================================================================
    # upload
    with open(test_file, 'rb') as file_reader:
        bytesflow = BytesIO(file_reader.read())
    ceph_conn.Object(bucket_name='EmailFile', key='/test/test').put(Body=bytesflow)

    # ==============================================================================
    # download
    ceph_conn.Object(bucket_name='EmailFile', key='/test/test').get()



