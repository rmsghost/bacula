variable "SG_ID" {
    type = string
    description = "Variavel que receberá o ID da subet"
}

variable "SUBNET_ID" {
    type = string
    description = "Variavel que receberá o ID da subet"
}

variable "INSTANCETYPE" {
    type = string
    default = "t2.micro"
    description = "Tipo de instancia para subir o projeto. O padrão é uma T2.MICRO, mas pode ser alterado"
}