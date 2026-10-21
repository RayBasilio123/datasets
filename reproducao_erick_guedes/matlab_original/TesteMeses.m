% Target
load('dados.mat', 'target')

% Para PCA
load('dados.mat', 'coeff')
load('dados.mat', 'mu')

% RNA normalizado
filename_ori = 'C:\Users\erick\Google Drive\Mestrado\Dissertação\Sandbox\Conceicao01\Delay\03-Marco\matlab\network_train0503.mat';
load(filename_ori);

testeY = net(medianaredfinalnorm15);

% RF normalizado
filename_ori = 'C:\Users\erick\Google Drive\Mestrado\Dissertação\Sandbox\Conceicao01\Experimentos\03-Marco\matlab\Relief\15\forest_3-500_train050.mat';
load(filename_ori);

yfit = trainedModel.predictFcn(medianaredfinalnorm15);


% Avaliação
mse = perform(net,target,testeY);
MSE_RF = immse(yfit',target)

plotregression(target,testeY);

f = figure;
plot(testeY);
hold on;
plot(target);

f = figure;
plot(movmean(testeY,5));
hold on;
plot(movmean(target,5));

Cyt = corrcoef(target,testeY);
R = Cyt(2,1)