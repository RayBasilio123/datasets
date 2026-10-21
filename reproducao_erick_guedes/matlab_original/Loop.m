% aleatorio = 0;
% alg_train = 0;
% for c = 1:100
% %     if c > 40 && mod(c,5) == 1
% %         aleatorio = 1;
% %     else
% %         aleatorio = 0;
% %     end
%     networ1_train001_code
%     DadosTreinamento_RFscore10_s_norm
%     Salva_R_Experimento
% end
% i = 0;


aleatorio = 1;
for c = 1:15
%     if 1 > 100
        alg_train = 1;
        if mod(c,5) == 1
            aleatorio = 1;
        else
            aleatorio = 0;
        end
        networ1_train001_code;
        
    %    alg_train = 0;
%         aleatorio = 0;
    %    networ1_train001_code;
%     end
    
    %DadosTreinamento_RFscore10_s_norm
    %DadosTreinamento_RF15_s_norm
    Salva_R_Experimento_b
end