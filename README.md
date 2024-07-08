:computer: STACK DE OBSERVABILIDADE :computer:
## _Projeto para estudo de metologias de monitoramento_

---
Este projeto consiste em subir uma Stack de observabilidade e estudar seus principais conceitos, expondo a prática alinhada com metologias.
---

## Descrição - Resumo geral

Será usado neste projeto: AWS, Terraform, Docker, Python, Grafana, Prometheus, Jaegger e cAdvisor. A base desse projeto é a API em Python, simulando uma aplicação com conexões simples com um banco de dados (mysql) onde através dela será possível consultar um pokemon pelo ID da Pokedex.
Essa API irá funcionar de forma containerizada, juntamente com toda a sua Stack. 

## Features
- API retorna o nome de um Pokemon com base em seu ID da National Pokedex. 

## Stack de observabilidade

A API será monitorada utilizando o Prometheus e Jaeger: 

- Jaeger: Irá monitorar os tracings da aplicação. No código estão exemplos de instrumentalização manual e automática.
- Prometheus: Irá expor métricas customizáveis da aplicação. No código estão exemplos de instrumentalização manual e exposição automática
- Grafana: Irá conter dashboards para visualização de dados expostos pelo Prometheus e pelo cAdvisor
= cAdvisor: Funcionará para coletar métricas do estado dos containers, garantindo monitorando de CPU, Memória e disco deles.


## Infraestrutura

Todo esse projeto poderá rodar localmente em uma máquina que contenha as versões mais atualizadas do Docker e Docker compose, porém, esta primeira versão foi pensada para rodar em uma EC2 na AWS. As futuras versões irão rodar em Kubernetes e (talvez) Elastic Beanstalk/ECS. As instruções par os SETUPS estão abaixo:

## SETUP :AWS: - RODANDO EM AWS EC2

Para rodar esse projeto em uma EC2, será necessáiro provisionar uma instância T2.Micro (para se manter no free tier, porém, poderá ter problema de performance com os containers, comento isso na sessão "Performance issues" logo abaixo). O arquivo "main.tf" conterá uma infraestrutura básica na AWS com os seguintes elementos: 

- VPC + 1 subnet pública + Route table
- 1 Security group (beeem permissivo, leia o código antes de aplica-lo em sua conta.)
- Internet Gateway
- 1 EC2

## Infraestrutura - Particularidade da EC2
A EC2 já sobe com um setup (via terraform mesmo) para instalação do Docker e do Docker-compose. Para isso, é necessário criar uma Chave privada, adiciona-la no seu repositório ou localmente, e aponta-la na linha 120 do arquivo "main.tf". Optei por fazer assim para testar um conceito, porém não é o melhor modo de fazer. Você pode usar o "user data" junto com o Terraform. Basta retirar o trecho de código da linha 117 até a linha 135 do arquivo "main.tf" e adicionar a linha abaixo. Dessa forma é muito mais seguro do que usar uma chave EC2 e mais automático:

```
user_data = "${file("script.sh")}"
```

## Peformance Issues:
Com uma instancia t2.micro, os containers poderão rodar com lentidão devido ao comportilhamento de memória. Pensando nisso, você pode alterar o compose.yaml definindo uma sessão de "deploy" para controlar o memória RAM provisionada. Nessa versão do projeto, limitei apenas o container do banco de dados. Basta reproduzir as mesmas linhas de código para cada container. Se atente ao recomendável para os containers como Grafana, cAdvisor e Prometheus. As aplicações não consomem nada de memória. 


## Installation
Presumo que tenha o terraform instalado em sua máquina, caso não tenha, veja o link: [## Install terraform](https://developer.hashicorp.com/terraform/install).
Com o terraform pronto, você precisará criar três variáveis de ambiente (ou poderá utilizar a configuração padrão do seu AWSCLI instalada em sua máquina). As variáveis são:

```
# export AWS_ACCESS_KEY_ID="anaccesskey"
# export AWS_SECRET_ACCESS_KEY="asecretkey"
# export AWS_REGION="us-west-2"
```

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Plugins

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```

## Docker

Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd dillinger
docker build -t <youruser>/dillinger:${package.json.version} .
```

This will create the dillinger image and pull in the necessary dependencies.
Be sure to swap out `${package.json.version}` with the actual
version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
