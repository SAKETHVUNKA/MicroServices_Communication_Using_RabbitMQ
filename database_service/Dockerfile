# Use the official MySQL image
FROM mysql:8.0  

# Set environment variable for the root password (replace with a strong password)
ENV MYSQL_ROOT_PASSWORD=mypassword

# Expose the default MySQL port
EXPOSE 3306

# Create a persistent volume for data
VOLUME /var/lib/mysql

# Define service configuration at startup
CMD ["mysqld"]
#  mysql -h localhost -P 3307 -u root -pmypassword