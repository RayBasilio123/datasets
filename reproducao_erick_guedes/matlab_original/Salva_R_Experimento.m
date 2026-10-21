% Matriz onde salvar os dados
if exist('experimentos','var') == 0
    experimentos = [0 0 0 0 0 0 0 0 0 0 0 0 0];
end

% Número do experimento
if exist('i','var') == 0
    i = 0;
end
i = i + 1

% Targets e Saídas do treinamento
% RNA
tr_t = target(:,indicesTrain);
tr_y_lm = y_lm(:,indicesTrain);
tr_y_scg = y_scg(:,indicesTrain);


% Cálculo do coeficiente de correlação linear do treinamento
% RNA
Cyt_lm = corrcoef(tr_y_lm,tr_t);
R_tr_lm = Cyt_lm(2,1);
Cyt_scg = corrcoef(tr_y_scg,tr_t);
R_tr_scg = Cyt_scg(2,1);
% RF
Cyt = corrcoef(y_train,t_treinamento);
R_tr_rf = Cyt(2,1);

% Targets e Saídas do Teste
% RNA
te_t = target(:,indicesTest);
te_y_lm = y_lm(:,indicesTest);
te_y_scg = y_scg(:,indicesTest);

% Cálculo do coeficiente de correlação linear do treinamento
% RNA
Cyt_lm = corrcoef(te_y_lm,te_t);
R_te_lm = Cyt_lm(2,1);
Cyt_scg = corrcoef(te_y_scg,te_t);
R_te_scg = Cyt_scg(2,1);
% RF
Cyt = corrcoef(y_test,t_teste);
R_te_rf = Cyt(2,1);

% Targets e Saídas de todos os dados
%td_t = target;
td_y_lm = y_lm(:,indicesTest);
td_y_scg = y_scg(:,indicesTest);

% Cálculo do coeficiente de correlação linear de todos os dados
% RNA
Cyt_lm = corrcoef(target,y_lm);
R_ge_lm = Cyt_lm(2,1);
Cyt_scg = corrcoef(target,y_scg);
R_ge_scg = Cyt_scg(2,1);
% RF
Cyt = corrcoef(y_geral,target);
R_ge_rf = Cyt(2,1);

% j = i;
% while R_te_lm < 0 || isnan(R_te_lm)
%     i = j - 1;
%     networ1_train001_code
%     
%     tr_t = target(:,indicesTrain);
%     tr_y = y(:,indicesTrain);
%     Cyt = corrcoef(tr_y,tr_t);
%     R_tr = Cyt(2,1);
%     
%     te_t = target(:,indicesTest);
%     te_y = y(:,indicesTest);
%     Cyt = corrcoef(te_y,te_t);
%     R_te = Cyt(2,1);
%     
%     Cyt = corrcoef(target,y);
%     R_ge = Cyt(2,1);
%     
%     repeticoes = repeticoes + 1;
% end
% i = j;

experimentos = [experimentos; i R_tr_lm R_te_lm R_ge_lm performance_lm R_tr_scg R_te_scg R_ge_scg performance_scg R_tr_rf R_te_rf R_ge_rf MSE_RF];

% Plota gráficos de regressão
% RF
%plotregression(t_treinamento,y_train,'Training',t_teste,y_test,'Test',target,y_geral,'All');
% RNA
%plotregression(tr_t,tr_y,'Training',te_t,te_y,'Test',target,y,'All');
