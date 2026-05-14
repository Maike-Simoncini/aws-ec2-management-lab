#!/bin/bash
# Atualiza o sistema e instala o servidor Apache
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Cria uma página personalizada para identificar a instância
echo "<h1>Instancia EC2 Gerenciada via Automacao</h1>" > /var/www/html/index.html
