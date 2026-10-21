% Carregar divisão de dados do experimento com trainlm para treinar com
% trainscg
%if aleatorio == 0
if i < 100
    filename_ori = 'C:\Users\erick\Google Drive\Mestrado\Dissertação\Sandbox\Conceicao01\Experimentos\03-Marco\matlab\Relief\15\subsets_train0';
    %filename_ori = 'C:\Users\erick\Google Drive\Mestrado\Dissertação\Sandbox\Conceicao01\Experimentos\03-Marco\matlab\PCA\subsets_train0';
    %filename_ori = 'C:\Users\erick\Google Drive\Mestrado\Dissertação\Sandbox\Conceicao01\Experimentos\03-Marco\matlab\Relief\17\subsets_train0';
    j = i + 1;
    if j >= 10
       filename_ori = sprintf('%s%d.mat',filename_ori,j);
    else
       filename_ori = sprintf('%s%d%d.mat',filename_ori,0,j);
    end
    load(filename_ori);
end


% Gera conjuntos de treinamento com base na divisão realizada durante o
% desenvolvimento da RNA
treinamento_rf = [input_final_norm15(:,indicesTrain), input_final_norm15(:,indicesVal)];
t_treinamento = [target(:,indicesTrain), target(:,indicesVal)];

treinamento_rf = [treinamento_rf; t_treinamento];

% Treina o modelo gerado pelo Regression Learner App com o conjunto de
% treinamneto utilizado na RNA (treinamento + validação)
[trainedModel, validationRMSE] = forest_code_15(treinamento_rf);

% Cria um vetor com os valores de predições do modelo para o conjunto de
% dados usado no treinamento
y_train = trainedModel.predictFcn(treinamento_rf(1:size(treinamento_rf,1)-1,:));

% Plota o gráfico de regressão usando os dados de treinamento
%plotregression(t_treinamento,y_train,'Training');

%%
% Gera conjuntos de testes com base na divisão realizada durante o
% desenvolvimento da RNA
teste_rf = input_final_norm15(:,indicesTest);
t_teste = target(:,indicesTest);

% Faz predições para o conjunto de testes utilizando o modelo treinado
y_test = trainedModel.predictFcn(teste_rf);

% Plota o gráfico de regressão usando os dados de testes
%plotregression(t_teste,y_test,'Test');

%%
% Faz predições para o conjunto de todos os dados
y_geral = trainedModel.predictFcn(input_final_norm15);

% Plota o gráfico de regressão usando todos os dados
%plotregression(target,y_geral,'All');

% Plota os três gráficos de regressão
%plotregression(t_treinamento,y_train,'Training',t_teste,y_test,'Test',target,y_geral,'All');

%MSE_RNA = immse(y,target);

MSE_RF = immse(y_geral',target)

% Número do experimento
if exist('i','var') == 0
    % Se i não existe, salva com nome genérico
    filename_rf = sprintf('%s','forest_3-500_train0xx');
else
   % Se i existe, salva com próximo número
   j = i + 1;
   if j >= 10
       filename_rf = sprintf('%s%d','forest_3-500_train0',j);
   else
       filename_rf = sprintf('%s%d','forest_3-500_train00',j);
   end
end

% Salva os dados do experimento em uma matriz
%Salva_R_Experimento
 
save(filename_rf,'trainedModel');