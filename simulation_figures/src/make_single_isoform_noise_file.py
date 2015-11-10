import sys
sys.path.append("/Users/joazofeifa/Lab/interval_searcher/")
import node
def load_refSeqs(FILE):
	G ={}
	with open(FILE) as FH:
		for line in FH:
			chrom,start, stop, gene 	= line.strip("\n").split("\t")
			start, stop 	= int(start), int(stop)
			if chrom not in G:
				G[chrom]=list()
			G[chrom].append((int(start), int(stop), gene))
	for chrom in G:
		G[chrom].sort()
		G[chrom]=node.tree(G[chrom])
	return G
def load_FS(FILE):
	G ={}
	with open(FILE) as FH:
		for line in FH:
			chrom,start, stop 	= line.strip("\n").split("\t")[:3]
			start,stop 			= int(start),int(stop)
			if chrom not in G:
				G[chrom]=list()
			G[chrom].append((start, stop))
	return G

def filter_only_single_look_for_noise(A,B, OUT=""):
	keepers 	= list()
	noise_t 	= 3000
	t 			= 0
	for chrom in A:
		if chrom in B:
			T 		= A[chrom]
			b 		= B[chrom]
			for i in range(1, len(b)):
				FINDS  	= T.searchInterval((b[i][0], b[i][1]))
				if len(FINDS)==1 and b[i][1]-b[i][0] > 5000:
					keepers.append((chrom, b[i][0], b[i][1], FINDS[0][2]))
				if t < noise_t:
					off 	= b[i-1][1], b[i][0]
					FINDS 	= T.searchInterval((off[0], off[1]))
					if not FINDS:

						keepers.append((chrom, off[0],off[1], 0))
						t+=1
	FHW=open(OUT,"w")
	for chrom,start, stop, ID in keepers:
		if ID==0:
			ID="NOISE"
		FHW.write(chrom+"\t" + str(start)+"\t" + str(stop) + "\t" + ID + "\n")





if __name__ == "__main__":
	FS_MERGED 	= "/Users/joazofeifa/Lab/gro_seq_files/HCT116/interval_files/DMSO2_3_merged_FS.bed"
	REF 		= "/Users/joazofeifa/Lab/genome_files/RefSeqHG19.bed"
	OUT 		= "/Users/joazofeifa/Lab/gro_seq_files/HCT116/interval_files/single_isoform.bed"
	F 			= load_FS(FS_MERGED)
	R 			= load_refSeqs(REF)
	filter_only_single_look_for_noise(R,F, OUT=OUT)
	pass