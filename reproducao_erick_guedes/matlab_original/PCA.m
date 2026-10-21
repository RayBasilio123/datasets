% Aplica o PCA
[coeff,scoreTrain,latent,~,explained,mu] = pca(input_pre_relieff');

% Seleciona os 10 primeiros PC
scoreTrain10 = scoreTrain(:,1:10);

% Ajusta as dimensões das matrizes
scoreTrain = scoreTrain';
scoreTrain10 = scoreTrain10';
scoreTrain10_randFor = scoreTrain10_randFor';
scoreTrain21 = scoreTrain21';

% Treina a RNA
networ1_train001_code

%%

% Transforma os dados de teste de acordo com os PC encontrados
scoreTeste = (input_teste'-mu)*coeff;

% Aplica o modelo aos novos dados
testeY = net(scoreTeste');
plotregression(target_teste,testeY);