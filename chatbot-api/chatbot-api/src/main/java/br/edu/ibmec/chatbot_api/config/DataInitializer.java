package br.edu.ibmec.chatbot_api.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import br.edu.ibmec.chatbot_api.models.Cliente;
import br.edu.ibmec.chatbot_api.models.ReservaVoo;
import br.edu.ibmec.chatbot_api.models.ReservaHospedagem;
import br.edu.ibmec.chatbot_api.repository.ClienteRepository;
import br.edu.ibmec.chatbot_api.repository.ReservaVooRepository;
import br.edu.ibmec.chatbot_api.repository.ReservaHospedagemRepository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private ClienteRepository clienteRepository;
    
    @Autowired
    private ReservaVooRepository reservaVooRepository;
    
    @Autowired
    private ReservaHospedagemRepository reservaHospedagemRepository;

    @Override
    public void run(String... args) throws Exception {
        // Criar clientes de teste
        Cliente cliente1 = new Cliente();
        cliente1.setNome("João Silva");
        cliente1.setEmail("joao.silva@email.com");
        cliente1.setCpf("123.456.789-00");
        cliente1.setTelefone("(11) 99999-9999");
        cliente1 = clienteRepository.save(cliente1);

        Cliente cliente2 = new Cliente();
        cliente2.setNome("Maria Santos");
        cliente2.setEmail("maria.santos@email.com");
        cliente2.setCpf("987.654.321-00");
        cliente2.setTelefone("(21) 88888-8888");
        cliente2 = clienteRepository.save(cliente2);

        // Criar reservas de voo de teste
        ReservaVoo voo1 = new ReservaVoo();
        voo1.setClienteId(cliente1.getId());
        voo1.setOrigem("São Paulo (GRU)");
        voo1.setDestino("Rio de Janeiro (GIG)");
        voo1.setDataHoraPartida(LocalDateTime.of(2025, 11, 15, 8, 30));
        voo1.setDataHoraChegada(LocalDateTime.of(2025, 11, 15, 10, 30));
        voo1.setCompanhiaAerea("LATAM");
        voo1.setNumeroVoo("LA3001");
        voo1.setAssento("12A");
        voo1.setClasse("ECONOMICA");
        voo1.setPreco(new BigDecimal("450.00"));
        voo1.setStatus("CONFIRMADA");
        reservaVooRepository.save(voo1);

        ReservaVoo voo2 = new ReservaVoo();
        voo2.setClienteId(cliente2.getId());
        voo2.setOrigem("Rio de Janeiro (GIG)");
        voo2.setDestino("Brasília (BSB)");
        voo2.setDataHoraPartida(LocalDateTime.of(2025, 12, 20, 14, 15));
        voo2.setDataHoraChegada(LocalDateTime.of(2025, 12, 20, 16, 45));
        voo2.setCompanhiaAerea("GOL");
        voo2.setNumeroVoo("G31045");
        voo2.setAssento("18C");
        voo2.setClasse("ECONOMICA");
        voo2.setPreco(new BigDecimal("320.00"));
        voo2.setStatus("PENDENTE");
        reservaVooRepository.save(voo2);

        // Criar reservas de hospedagem de teste
        ReservaHospedagem hotel1 = new ReservaHospedagem();
        hotel1.setClienteId(cliente1.getId());
        hotel1.setNomeHotel("Hotel Copacabana Palace");
        hotel1.setCidade("Rio de Janeiro");
        hotel1.setEndereco("Av. Atlântica, 1702 - Copacabana");
        hotel1.setDataCheckIn(LocalDate.of(2025, 11, 15));
        hotel1.setDataCheckOut(LocalDate.of(2025, 11, 18));
        hotel1.setTipoQuarto("DELUXE");
        hotel1.setNumeroQuarto("1205");
        hotel1.setNumeroHospedes(2);
        hotel1.setPrecoPorNoite(new BigDecimal("850.00"));
        hotel1.setPrecoTotal(new BigDecimal("2550.00"));
        hotel1.setStatus("CONFIRMADA");
        hotel1.setTelefoneHotel("(21) 2548-7070");
        hotel1.setEmailHotel("reservas@copacabanapalace.com");
        reservaHospedagemRepository.save(hotel1);

        ReservaHospedagem hotel2 = new ReservaHospedagem();
        hotel2.setClienteId(cliente2.getId());
        hotel2.setNomeHotel("Hotel Nacional Brasília");
        hotel2.setCidade("Brasília");
        hotel2.setEndereco("SHTN Trecho 01 Conjunto 1 Bloco A");
        hotel2.setDataCheckIn(LocalDate.of(2025, 12, 20));
        hotel2.setDataCheckOut(LocalDate.of(2025, 12, 22));
        hotel2.setTipoQuarto("STANDARD");
        hotel2.setNumeroHospedes(1);
        hotel2.setPrecoPorNoite(new BigDecimal("280.00"));
        hotel2.setPrecoTotal(new BigDecimal("560.00"));
        hotel2.setStatus("PENDENTE");
        hotel2.setTelefoneHotel("(61) 3429-8000");
        hotel2.setEmailHotel("reservas@hotelnacional.com.br");
        reservaHospedagemRepository.save(hotel2);

        System.out.println("=== DADOS DE TESTE CARREGADOS ===");
        System.out.println("Clientes criados: " + clienteRepository.count());
        System.out.println("Reservas de voo criadas: " + reservaVooRepository.count());
        System.out.println("Reservas de hospedagem criadas: " + reservaHospedagemRepository.count());
        System.out.println("=================================");
    }
}