# Base image
FROM debian:latest

# Install the required packages for Kerberos
RUN apt-get update && apt-get install -y \
    krb5-kdc \
    krb5-admin-server \
    krb5-config \
    && rm -rf /var/lib/apt/lists/*

# Set up Kerberos environment variables (edit as needed)
ENV REALM REALM1.LOCAL
ENV KDC_DOMAIN localhost

# Copy your krb5.conf and KDC configuration (if needed)
COPY krb5_conf/krb5.conf /etc/krb5.conf

# Expose necessary Kerberos ports
EXPOSE 88 749

# Set the KDC database directory
VOLUME /var/lib/kerberos/krb5kdc

# Command to start the Kerberos KDC and admin server
CMD /usr/sbin/krb5kdc && /usr/sbin/kadmind -nofork
