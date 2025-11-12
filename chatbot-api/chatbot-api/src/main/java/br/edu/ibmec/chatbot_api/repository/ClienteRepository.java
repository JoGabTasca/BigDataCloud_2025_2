package br.edu.ibmec.chatbot_api.repository;

import java.util.List;

import org.springframework.stereotype.Repository;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import com.azure.spring.data.cosmos.repository.Query;

import br.edu.ibmec.chatbot_api.models.Cliente;
import java.util.Optional;

@Repository // Indica que essa interface é um repositório do banco de dados
public interface ClienteRepository extends CosmosRepository<Cliente, String> {

    // Busca cliente por CPF
    Optional<Cliente> findByCpf(String cpf);

    // Query personalizada para buscar todos os clientes
    // A query no Cosmos DB usa "c" como alias e o nome do container
    @Query("SELECT * FROM clientes c")
    List<Cliente> findAllClientes();
}


