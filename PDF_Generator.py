from ParticleAnalyzer import ParticleAnalyzer
class PDF_Generator:
    test = ParticleAnalyzer()

    print ' '

    print 'This program displays the probability density function (PDF) for a set sequence length.'
    print 'WARNING: Constructing a PDF for lengths greater than 20 will take multiple minutes.'

    again = True

    while again:

        print ' '
        seqLen = input('Enter sequence length as a positive integer: ')
        

        test.findPDF(seqLen)

        print ' '

        answer = raw_input('Generate another PDF? (Y/N): ')

        if answer == 'Y':
            again = True
        else:
            again = False
