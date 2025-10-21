package br.edu.ibmec.chatbot_api.models;
import java.util.List;

import org.springframework.data.annotation.Id;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;

import lombok.Data;

@Data // Gera getters, setters, toString, equals e hashCode automaticamente
@Container(containerName = "clientes")
public class Cliente {

    @Id
    private String id;

    private String nome;

    private String email;

    @PartitionKey
    private String cpf;

    private String telefone;

    private List<ReservaVoo> reservasVoo;

    private List<ReservaHospedagem> reservasHospedagem;
}
