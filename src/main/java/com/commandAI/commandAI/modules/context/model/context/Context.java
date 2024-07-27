    package com.commandAI.commandAI.modules.context.model.context;
    import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
    import jakarta.persistence.*;
    import lombok.Data;

    import java.time.LocalDateTime;
    @Data
    @Table(name = "tb_context")
    @Entity
    @JsonIgnoreProperties(ignoreUnknown = true)
    public class Context {

        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @Column(name = "context", nullable = false, columnDefinition = "TEXT")
        private String context;

        @Column(name = "created_at", nullable = false)
        private LocalDateTime createdAt;

        @PrePersist
        protected void onCreate() {
            createdAt = LocalDateTime.now();
        }
    }

