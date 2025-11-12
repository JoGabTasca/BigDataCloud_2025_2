package br.edu.ibmec.chatbot_api.models;
import java.util.List;

import org.springframework.data.annotation.Id;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data // Gera getters, setters, toString, equals e hashCode automaticamente
@Container(containerName = "clientes")
public class Cliente {

    @Id
    @JsonProperty("id")
    private String id;

    @JsonProperty("nome")
    private String nome;

    @JsonProperty("email")
    private String email;

    @PartitionKey
    @JsonProperty("cpf")
    private String cpf;

    @JsonProperty("telefone")
    private String telefone;

    @JsonProperty("reservasVoo")
    private List<ReservaVoo> reservasVoo;

    @JsonProperty("reservasHospedagem")
    private List<ReservaHospedagem> reservasHospedagem;

}
